from CfbGame import CfbGame
import sqlite3
class CfbGameDb:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._cur = self._conn.cursor()

        self._ddl = """
            CREATE TABLE IF NOT EXISTS games (
                id                      INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id                 INTEGER,
                opponent_id             INTEGER,
                season                  INTEGER,
                game_type               TEXT,
                date                    TEXT,  -- ISO 8601
                team_rank               INTEGER,
                team                    TEXT,
                team_conf               TEXT,
                team_division           TEXT,
                coach                   TEXT,
                team_spread             REAL,
                site                    TEXT,
                opp_rank                INTEGER,
                opponent                TEXT,
                opp_conf                TEXT,
                opp_division            TEXT,
                opp_coach               TEXT,
                opp_spread              REAL,
                result                  TEXT,
                team_points             INTEGER,
                opp_points              INTEGER,
                points_diff             INTEGER,
                total_points            INTEGER,
                team_season_id          INTEGER,
                team_game_no            INTEGER,
                underdog_favorite       TEXT,
                covered                 TEXT,
                team_wins_entering      INTEGER,
                team_losses_entering    INTEGER,
                team_ties_entering      INTEGER,
                opp_wins_entering       INTEGER,
                opp_losses_entering     INTEGER,
                opp_ties_entering       INTEGER,
                over_under              REAL,
                over_or_under_result    TEXT,
                FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
                FOREIGN KEY (opponent_id) REFERENCES teams(id) ON DELETE CASCADE
            );
            """


        self._insert_sql = """
        INSERT INTO games (
            team_id, opponent_id,
            season, game_type, date,
            team_rank, team, team_conf, team_division, coach,
            team_spread, site,
            opp_rank, opponent, opp_conf, opp_division, opp_coach,
            opp_spread, result,
            team_points, opp_points, points_diff, total_points,
            team_season_id, team_game_no,
            underdog_favorite, covered,
            team_wins_entering, team_losses_entering, team_ties_entering,
            opp_wins_entering, opp_losses_entering, opp_ties_entering,
            over_under, over_or_under_result
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

    def table_exists(self, table_name: str) -> bool:
        try:
            self._cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                (table_name,)
            )
            return self._cur.fetchone() is not None
        except Exception as e:
            print(f"[error] Failed to check if table '{table_name}' exists: {e}")
            return False

    def create_table_if_not_exists(self):
        if self.table_exists("games"):
            print("[info] Table 'games' already exists. Skipping creation.")
            return False
        print("[info] Creating table 'games'.")
        self._cur.executescript(self._ddl)
        self._conn.commit()
        return True

    def insert_game(self, game: CfbGame):
        try:
            values = game.to_db_tuple()
            self._cur.execute(self._insert_sql, values)
            self._conn.commit()
            # print("[info] Inserted game")
        except Exception as e:
            print(f"[error] Failed to insert game: {e}")

    def select_print_all(self):
        self._cur.execute("""
            SELECT g.*, t1.name as home_team, t2.name as away_team
            FROM games g
            JOIN teams t1 ON g.team_id = t1.id
            JOIN teams t2 ON g.opponent_id = t2.id
            ORDER BY g.id;
        """)
        rows = self._cur.fetchall()
        for row in rows:
            print(row)
        return rows

    def get_team_id_by_name(self, name: str):
        try:
            norm = (name or "").strip().lower()
            self._cur.execute(
                """
                SELECT id FROM teams
                WHERE LOWER(TRIM(name)) = ?
                """,
                (norm,)
            )
            row = self._cur.fetchone()
            if row:
                return row[0]
            else:
                print(f"[warn] Team not found: '{name}'")
                return None
        except Exception as e:
            print(f"[error] Failed to fetch team ID for '{name}': {e}")
            return None

    def game_exists(self, team_id: int, opponent_id: int, date: str):
        try:
            self._cur.execute(
                """
                SELECT 1 FROM games
                WHERE team_id = ? AND opponent_id = ? AND date = ?
                """,
                (team_id, opponent_id, date),
            )
            return self._cur.fetchone() is not None
        except Exception as e:
            print(f"[error] Failed to check game existence: {e}")
            return False


    def close(self):
        try:
            if self._conn:
                self._conn.close()
                self._conn = None
                print("Closed connection")
        except Exception as e:
            print(f"Error Exception: {e}")


