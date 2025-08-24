import sqlite3
from utilities import cfb_tricodes
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Optional
from dateutil import parser   # more flexible date parsing
class BetFinder:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def did_cover(
        self,
        team_name: str,
        start_year: int,
        end_year: int,
        covered_value: str = "yes",
        conferences: Optional[List[str]] = None
    ) -> Optional[float]:
        """
        Returns the percentage of games where `team_name` covered the spread 
        between `start_year` and `end_year`.

        Assumes 'covered' field is a string ("yes", "no", etc.).

        If `conferences` is provided, only include games where opp_conf is in that list.
        """
        base_query = """
            SELECT COUNT(*) as total_games,
                SUM(CASE WHEN LOWER(covered) = LOWER(?) THEN 1 ELSE 0 END) as covered_games
            FROM games
            WHERE team = ?
            AND season BETWEEN ? AND ?
        """

        params: List = [covered_value, team_name, start_year, end_year]

        # Add conference filter if provided
        if conferences:
            placeholders = ",".join(["?"] * len(conferences))
            base_query += f" AND opp_conf IN ({placeholders})"
            params.extend(conferences)

        cur = self.conn.cursor()
        cur.execute(base_query, params)
        row = cur.fetchone()

        total = row["total_games"]
        covered = row["covered_games"]

        if total == 0:
            print(f"[warn] No games found for team '{team_name}' between {start_year} and {end_year}")
            return None

        return round((covered / total) * 100, 2)
    
    def win_loss_record(
            self,
            team_name: str,
            start_year: int,
            end_year: int
        ):
        """
        Returns win/loss/tie record for the team between seasons,
        based on team_points vs opp_points.
        """
        query = """
        SELECT
            SUM(CASE WHEN team_points > opp_points THEN 1 ELSE 0 END) AS wins,
            SUM(CASE WHEN team_points < opp_points THEN 1 ELSE 0 END) AS losses,
            SUM(CASE WHEN team_points = opp_points THEN 1 ELSE 0 END) AS ties,
            COUNT(*) AS total
        FROM games
        WHERE team = ?
        AND season BETWEEN ? AND ?
        AND team_points IS NOT NULL
        AND opp_points IS NOT NULL
        """

        cur = self.conn.cursor()
        cur.execute(query, (team_name, start_year, end_year))
        row = cur.fetchone()

        return {
            "wins": row["wins"] or 0,
            "losses": row["losses"] or 0,
            "ties": row["ties"] or 0,
            "total": row["total"] or 0,
        }

    def spread_deltas(
            self,
            team_name: str,
            start_year: int,
            end_year: int
        ):
        """
        Returns a list of dictionaries showing how far off the closing spread
        (team_spread) was from the actual result (opp_points - team_points)
        for each game between the given years.
        """
        query = """
        SELECT
            date,
            season,
            team,
            opponent,
            team_points,
            opp_points,
            team_spread
        FROM games
        WHERE team = ?
        AND season BETWEEN ? AND ?
        AND team_spread IS NOT NULL
        AND team_points IS NOT NULL
        AND opp_points IS NOT NULL
        ORDER BY date ASC
        """

        cur = self.conn.cursor()
        cur.execute(query, (team_name, start_year, end_year))
        rows = cur.fetchall()

        results = []

        for row in rows:
            predicted = row["team_spread"]
            actual_spread = row["opp_points"] - row["team_points"]
            delta = predicted - actual_spread  # positive = underdog underperformed
            results.append({
                "date": row["date"],
                "season": row["season"],
                "team": row["team"],
                "opponent": row["opponent"],
                "team_points": row["team_points"],
                "opp_points": row["opp_points"],
                "closing_spread": predicted,
                "actual_spread": actual_spread,
                "delta": round(delta, 2)
            })

        return results

    def did_hit_over_under(
        self,
        team_name: str,
        start_year: int,
        end_year: int,
        result_value: str = "over",
        conferences: Optional[List[str]] = None
    ):
        """
        Returns the percentage of games where the over/under result matched the given value.
        Valid result_value: "over", "under", "push"

        If `conferences` is provided, only include games where opp_conf is in that list.
        """
        base_query = """
            SELECT COUNT(*) as total_games,
                SUM(CASE WHEN LOWER(over_or_under_result) = LOWER(?) THEN 1 ELSE 0 END) as matching_result
            FROM games
            WHERE team = ?
            AND season BETWEEN ? AND ?
            AND over_or_under_result IS NOT NULL
        """

        params: list = [result_value, team_name, start_year, end_year]

        # Add conference filter if provided
        if conferences:
            placeholders = ",".join(["?"] * len(conferences))
            base_query += f" AND opp_conf IN ({placeholders})"
            params.extend(conferences)

        cur = self.conn.cursor()
        cur.execute(base_query, params)
        row = cur.fetchone()

        total = row["total_games"]
        matched = row["matching_result"]

        if total == 0:
            return None

        return round((matched / total) * 100, 2)

    def total_points_deltas(
            self,
            team_name: str,
            start_year: int,
            end_year: int
        ):
            """
            Returns a list of dictionaries comparing predicted total points (over_under)
            to actual total points (team_points + opp_points) for each game.
            """
            query = """
            SELECT
                date,
                season,
                team,
                opponent,
                team_points,
                opp_points,
                over_under,
                over_or_under_result
            FROM games
            WHERE team = ?
            AND season BETWEEN ? AND ?
            AND over_under IS NOT NULL
            AND team_points IS NOT NULL
            AND opp_points IS NOT NULL
            ORDER BY date ASC
            """
            cur = self.conn.cursor()
            cur.execute(query, (team_name, start_year, end_year))
            rows = cur.fetchall()

            results = []

            for row in rows:
                actual_total = row["team_points"] + row["opp_points"]
                predicted_total = row["over_under"]
                delta = actual_total - predicted_total  # positive = game went over expected total

                results.append({
                    "date": row["date"],
                    "season": row["season"],
                    "team": row["team"],
                    "opponent": row["opponent"],
                    "team_points": row["team_points"],
                    "opp_points": row["opp_points"],
                    "actual_total": actual_total,
                    "predicted_total": predicted_total,
                    "delta": round(delta, 2),
                    "result": row["over_or_under_result"]
                })

            return results
    
    def did_hit_over_under_in_date_window(
        self,
        start_year: int,
        end_year: int,
        start_mmdd: str,   # e.g. "09/01"
        end_mmdd: str,     # e.g. "09/30"
        team_name: Optional[str] = None,
        conferences: Optional[List[str]] = None
    ) -> Optional[dict]:
        """
        Returns the percentage of games that went OVER, UNDER, or PUSH in the given date window and year range.

        If `team_name` is given, filters to that team only.
        If `conferences` are given, filters to those opponent conferences.
        """
        query = """
            SELECT date, over_under, total_points
            FROM games
            WHERE season BETWEEN ? AND ?
            AND over_under IS NOT NULL
            AND total_points IS NOT NULL
        """
        params: List = [start_year, end_year]

        if team_name:
            query += " AND team = ?"
            params.append(team_name)

        if conferences:
            placeholders = ",".join(["?"] * len(conferences))
            query += f" AND opp_conf IN ({placeholders})"
            params.extend(conferences)

        cur = self.conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()

        if not rows:
            print("[warn] No games matched your filters.")
            return None

        start_month, start_day = map(int, start_mmdd.split("/"))
        end_month, end_day = map(int, end_mmdd.split("/"))

        over, under, push, total = 0, 0, 0, 0

        for r in rows:
            game_date = parser.parse(r["date"])

            if start_year <= game_date.year <= end_year:
                start_window = datetime(game_date.year, start_month, start_day)
                end_window = datetime(game_date.year, end_month, end_day)

                if start_window <= game_date <= end_window:
                    closing = r["over_under"]
                    actual = r["total_points"]

                    # Skip if either value is None or empty string
                    if not closing or not actual:
                        continue

                    try:
                        closing_total = float(closing)
                        actual_total = float(actual)
                    except ValueError:
                        continue  # skip bad data

                    if actual_total > closing_total:
                        over += 1
                    elif actual_total < closing_total:
                        under += 1
                    else:
                        push += 1

                    total += 1

        if total == 0:
            print("[warn] No games matched within the date window.")
            return None

        return {
            "games": total,
            "over_pct": round(over / total * 100, 2),
            "under_pct": round(under / total * 100, 2),
            "push_pct": round(push / total * 100, 2),
            "over_count": over,
            "under_count": under,
            "push_count": push
        }


def analyze_teams(teams: List[str], start_year: int, end_year: int, bf: BetFinder, conferences: Optional[List[str]] = None):
    """
    Iterate over a list of teams and print spread/total stats for each.
    """

    assert start_year <= end_year, "start year must be less than or equal to end year"

    for team in teams:
        print(f"\n--- {team.upper()} ---")
        
        result = bf.did_cover(team, start_year, end_year, conferences=conferences)
        if result is not None:
            print(f"{team} covered the spread {result}% of the time.")

        over_pct = bf.did_hit_over_under(team, start_year, end_year, result_value="over", conferences=conferences)
        if over_pct is not None:
            print(f"{team} hit the **over** {over_pct}% of the time.")

        under_pct = bf.did_hit_over_under(team, start_year, end_year, result_value="under", conferences=conferences)
        if under_pct is not None:
            print(f"{team} hit the **under** {under_pct}% of the time.")


# Example usage:
if __name__ == "__main__":
    bf = BetFinder("cfb_database.db")  # update path to your SQLite DB
    teams = ["miami", "notre dame"] 
    # teams = ["ucla", "utah"]
    conferences = ["ACC", "PAC-12", "SEC", "Big Ten", "Big 12", "Independents"]
    # "syracuse", "tennessee", "florida atlantic", "alabama", "florida state", "coastal carolina", "virginia", "clemson", "lsu", "ucla", "utah"]
    start_year = 2023
    end_year = 2024
    analyze_teams(teams, start_year, end_year, bf, conferences)
    
    # result = bf.did_hit_over_under_in_date_window(
    #     start_year=2000,
    #     end_year=2024,
    #     start_mmdd="09/01",
    #     end_mmdd="09/30"
    # )

    # if result:
    #     print(f"Games analyzed: {result['games']}")
    #     print(f"Over hit: {result['over_pct']}%")
    #     print(f"Under hit: {result['under_pct']}%")
    #     print(f"Push: {result['push_pct']}%")

    # team = "ohio state"
    # assert start_year <= end_year, f"start year must be less than or equal to end year"
    # result = bf.did_cover(team, start_year, end_year)

    # if result is not None:
    #     print(f"{team} covered the spread  {result}% .")

    # over_pct = bf.did_hit_over_under(team, start_year, end_year, result_value="over")
    # if over_pct is not None:
    #     print(f"{team} hit the **over** {over_pct}% of the time.")

    # under_pct = bf.did_hit_over_under(team, start_year, end_year, result_value="under")
    # if under_pct is not None:
    #     print(f"{team} hit the **under** {under_pct}% of the time.")
    # # Win/loss record
    # record = bf.win_loss_record(team, start_year, end_year)
    # print(f"Win/Loss/Tie ({start_year} to {end_year}): {record['wins']}-{record['losses']}-{record['ties']} (Total: {record['total']})")

    # spread_errors = bf.spread_deltas(team, start_year, end_year)

    # # for game in spread_errors:
    # #     print(f"{game['date']} {game['team']} vs {game['opponent']} — "
    # #           f"Actual: {game['actual_spread']}, Closing: {game['closing_spread']}, "
    # #           f"Delta: {game['delta']}")
        
    # totals = bf.total_points_deltas(team, start_year, end_year)

    # for game in totals:
    #     print(f"{game['date']} {game['team']} vs {game['opponent']} — "
    #         f"Actual: {game['actual_total']}, Predicted: {game['predicted_total']}, "
    #         f"Delta: {game['delta']} ({game['result']})")
    
    # dates = [datetime.strptime(g["date"], "%m/%d/%y") for g in spread_errors]
    # deltas = [g["delta"] for g in spread_errors]
    # closing_spreads = [g["closing_spread"] for g in spread_errors]

    # total_deltas = [g["delta"] for g in totals]
    # closing_spreads = [g["predicted_total"] for g in totals]


    # # Plot
    # plt.figure(figsize=(12, 6))

    # # Actual - Predicted spread delta
    # plt.scatter(dates, deltas, color='blue', label="Spread Delta (Actual - Closing)", alpha=0.8)

    # # Closing spreads in red
    # plt.scatter(dates, closing_spreads, color='red', label="Closing Spread", alpha=0.6)

    # # Reference line at 0
    # plt.axhline(0, color='gray', linestyle='--', linewidth=1)

    # # Labels and layout
    # plt.title("Spread Deltas vs Closing Spread Over Time")
    # plt.xlabel("Game Date")
    # plt.ylabel("Points")
    # plt.xticks(rotation=45)
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # # --- Plot 2: Totals (Delta + Closing Spread) ---
    # plt.figure(figsize=(12, 6))
    # plt.scatter(dates, total_deltas, color='green', label="Total Delta (Actual - Closing)", alpha=0.8)
    # plt.scatter(dates, closing_spreads, color='red', label="Closing O/U", alpha=0.6)
    # plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    # plt.title("Total Deltas vs Closing O/U Over Time")
    # plt.xlabel("Game Date")
    # plt.ylabel("Points")
    # plt.xticks(rotation=45)
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()

    # # Show both figures
    # plt.show(block=False)

    # # Wait for user input, then close all
    # input("Press Enter to close the plots...")
    # plt.close("all")