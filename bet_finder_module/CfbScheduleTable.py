import sqlite3
from CfbSchedule import CfbSchedule
import json
class CfbScheduleTable:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._cur = self._conn.cursor()
        self._ddl = """
            CREATE TABLE IF NOT EXISTS schedule (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                home_team_id    INTEGER NOT NULL,
                away_team_id    INTEGER NOT NULL,
                game_date       TEXT NOT NULL,  -- ISO 8601
                week            INTEGER NOT NULL,
                season          INTEGER NOT NULL,
                FOREIGN KEY (home_team_id) REFERENCES teams(id) ON DELETE CASCADE,
                FOREIGN KEY (away_team_id) REFERENCES teams(id) ON DELETE CASCADE,
                UNIQUE(home_team_id, away_team_id, game_date)
            );
        """

        self._insert_sql = """
            INSERT INTO schedule (
                home_team_id,
                away_team_id,
                game_date,
                week,
                season
            ) VALUES (?, ?, ?, ?, ?);
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
        if self.table_exists("schedule"):
            print("[info] Table 'schedule' already exists. Skipping creation.")
            return False
        print("[info] Creating table 'schedule'.")
        self._cur.executescript(self._ddl)
        self._conn.commit()
        return True

    def insert_schedule_entry(self, home_team_id: int, away_team_id: int, game_date: str, week: int, season: int):
        try:
            self._cur.execute(self._insert_sql, (home_team_id, away_team_id, game_date, week, season))
            self._conn.commit()
            print(f"[info] Inserted: {home_team_id} vs {away_team_id} on {game_date}, week {week} season:{season}")
        except sqlite3.IntegrityError as e:
            print(f"[warn] Insert failed (likely duplicate): {e}")

    def insert_obj(self, obj: CfbSchedule):
        try:
            values = obj.to_db_tuple()
            self._cur.execute(self._insert_sql, values)
            self._conn.commit()
        except Exception as e:
            pass

    def select_print_all(self, team_name: str, season: int):
        try:
            team_id = self.get_team_id_by_name(team_name)
            if team_id is None:
                print(f"[warn] Team '{team_name}' not found. Cannot print schedule.")
                return []

            self._cur.execute("""
                SELECT 
                    s.id,
                    t1.team_name as home_team,
                    t2.team_name as away_team,
                    s.game_date,
                    s.week,
                    s.season
                FROM schedule s
                JOIN teams t1 ON s.home_team_id = t1.id
                JOIN teams t2 ON s.away_team_id = t2.id
                WHERE (s.home_team_id = ? OR s.away_team_id = ?)
                AND s.season = ?
                ORDER BY s.game_date;
            """, (team_id, team_id, season))

            rows = self._cur.fetchall()
            print(f"[info] Schedule for '{team_name.title()}', {season} season:")
            for row in rows:
                game_id, home, away, date, week, szn = row
                print(f"Week {week} | {date} | {home} vs {away}")

            return rows
        except Exception as e:
            print(f"[error] Failed to select schedule: {e}")
            return []
    
    def obj_exists(self, home_team_id: int, away_team_id: int, game_date: str, season: int):
        try:
            self._cur.execute(
                """
                SELECT 1 FROM schedule
                WHERE home_team_id = ? AND away_team_id = ? AND game_date = ? AND season = ?
                """,
                (home_team_id, away_team_id, game_date, season),
            )
            return self._cur.fetchone() is not None
        except Exception as e:
            return False

    def get_team_id_by_name(self, name: str):
        try:
            norm = (name or "").strip().lower()
            self._cur.execute(
                """
                SELECT id FROM teams
                WHERE LOWER(TRIM(team_name)) = ?
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
        
    def close(self):
        try:
            if self._conn:
                self._conn.close()
                self._conn = None
                print("Closed connection")
        except Exception as e:
            print(f"Error Exception: {e}")

if __name__=="__main__":
    database = "./new_database.db"
    conn = sqlite3.connect(database)
    sdb = CfbScheduleTable(conn)
    fcs_schedule = "./fcs_schedules.json"
    fbs_schedule = "./fbs_schedules.json"
    sdb.create_table_if_not_exists()
    with open(fbs_schedule, "r") as jsonfile:
        data = json.load(jsonfile)
        for k,v in data.items():
            season = v["season"]
            for scheduled_game in v["schedule"]:
                home_team_id = sdb.get_team_id_by_name(scheduled_game["home_team"].strip().lower())
                away_team_id = sdb.get_team_id_by_name(scheduled_game["away_team"].strip().lower())
                game_date = scheduled_game["date"]
                week = scheduled_game["week"]
                schedule_obj = CfbSchedule(home_team_id, away_team_id, game_date, week, season)
                sdb.insert_obj(schedule_obj)
    with open(fcs_schedule, "r") as jsonfile:
        data = json.load(jsonfile)
        for k,v in data.items():
            season = v["season"]
            for scheduled_game in v["schedule"]:
                home_team_id = sdb.get_team_id_by_name(scheduled_game["home_team"])
                away_team_id = sdb.get_team_id_by_name(scheduled_game["away_team"])
                game_date = scheduled_game["date"]
                week = scheduled_game["week"]
                schedule_obj = CfbSchedule(home_team_id, away_team_id, game_date, week, season)
    # with open(fbs_schedule, "r") as jsonfile:
    #     data = json.load(jsonfile)
    #     for k,v in data.items():
    #         sdb.select_print_all(k, 2025)
    
    sdb.close()


