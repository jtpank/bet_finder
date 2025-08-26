from CfbGame import CfbGame
from CfbGameDb import CfbGameDb
import csv
from pathlib import Path
import sqlite3
from utilities import cfb_tricodes, CsvKeys

invalid_cfb_set = set()
def parse_and_load(csv_path: Path, game_db: CfbGameDb):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        count_inserted = 0
        count_skipped = 0
        for row in reader:
            site = row[CsvKeys.SITE]
            if site is None or site == "" or site == " ":
                site = "N"
            assert site is not None and site in ["N", "V", "H"], f"Site is not valid {site}"
            season = row[CsvKeys.SEASON]
            game_type = row[CsvKeys.GAME_TYPE]
            date = row[CsvKeys.DATE]
            team_rank = row[CsvKeys.TEAM_RANK]
            team = row[CsvKeys.TEAM].lower().strip()
            team_conf = row[CsvKeys.TEAM_CONF].lower().strip()
            team_division = row[CsvKeys.TEAM_DIVISION]
            coach = row[CsvKeys.COACH].lower().strip()
            team_spread = row[CsvKeys.TEAM_SPREAD]
            opp_rank = row[CsvKeys.OPP_RANK]
            opponent = row[CsvKeys.OPPONENT].lower().strip()
            opp_conf = row[CsvKeys.OPP_CONF].lower().strip()
            opp_division = row[CsvKeys.OPP_DIVISION]
            opp_coach = row[CsvKeys.OPP_COACH].lower().strip()
            opp_spread = row[CsvKeys.OPP_SPREAD]
            result = row[CsvKeys.RESULT]
            team_points = row[CsvKeys.TEAM_POINTS]
            opp_points = row[CsvKeys.OPP_POINTS]
            points_diff = row[CsvKeys.POINTS_DIFF]
            total_points = row[CsvKeys.TOTAL_POINTS]
            team_season_id = row[CsvKeys.TEAM_SEASON_ID]
            team_game_no = row[CsvKeys.TEAM_GAME_NO]
            underdog_favorite = row[CsvKeys.UNDERDOG_FAVORITE].lower().strip()
            covered = row[CsvKeys.COVERED]
            team_wins_entering = row[CsvKeys.TEAM_WINS_ENTERING]
            team_losses_entering = row[CsvKeys.TEAM_LOSSES_ENTERING]
            team_ties_entering = row[CsvKeys.TEAM_TIES_ENTERING]
            opp_wins_entering = row[CsvKeys.OPP_WINS_ENTERING]
            opp_losses_entering = row[CsvKeys.OPP_LOSSES_ENTERING]
            opp_ties_entering = row[CsvKeys.OPP_TIES_ENTERING]
            over_under = row[CsvKeys.OVER_UNDER]
            over_or_under_result = row[CsvKeys.OVER_OR_UNDER_RESULT]
            # if team not in (k.lower().strip() for k in cfb_tricodes.keys()):
            #     if team not in invalid_cfb_set:
            #         invalid_cfb_set.add(team)
            #         print(f"{team} not valid!")
            #     continue
            # if opponent not in (k.lower().strip() for k in cfb_tricodes.keys()):
            #     if opponent not in invalid_cfb_set:
            #         invalid_cfb_set.add(opponent)
            #         print(f"{opponent} not valid!")
            #     continue
            # assert team in cfb_tricodes.keys(), f"{team} not valid"
            # assert opponent in cfb_tricodes.keys(), f"{opponent} not valid"


            team_id = game_db.get_team_id_by_name(team)
            opponent_id = game_db.get_team_id_by_name(opponent)

            game_obj = CfbGame(
                team_id, opponent_id, season, game_type, date, team_rank,
                team, team_conf, team_division, coach, team_spread, site,
                opp_rank, opponent, opp_conf, opp_division, opp_coach, 
                opp_spread, result, team_points, opp_points, points_diff, 
                total_points, team_season_id, team_game_no, underdog_favorite,
                covered, team_wins_entering, team_losses_entering, team_ties_entering,
                opp_wins_entering, opp_losses_entering, opp_ties_entering,
                over_under, over_or_under_result
            )

            # print(f"{team}: {team_id} vs {opponent}: {opponent_id}, {date}")

            if team_id is None or opponent_id is None:
                print(f"[warn] Skipping row due to unresolved team: {row}")
                continue

            if game_db.game_exists(team_id, opponent_id, date):
                # print(f"[info] Skipping existing game: {team}: {team_id} vs {opponent}: {opponent_id} on {date}")
                count_skipped += 1
                continue
            # construct game obj
            game_db.insert_game(game_obj)
            count_inserted += 1
        print(f"[info] {count_inserted} games inserted, {count_skipped} skipped (already existed).")

def main():
    conn = sqlite3.connect("./new_database.db")
    game_db = CfbGameDb(conn)
    # game_db.create_table_if_not_exists()
    # csv_path = Path("../database/cfb_db_2024_normalized.csv")
    # parse_and_load(csv_path=csv_path, game_db=game_db)
    game_db.select_print_all()
    game_db.close()

if __name__=="__main__":
    main()
