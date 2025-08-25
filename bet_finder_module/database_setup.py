import sqlite3
import json
import csv
from utilities import cfb_tricodes
from pathlib import Path

class DataParser:
    def __init__(self):
        pass


class  CfbTeamDb:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._cur = self._conn.cursor()
        self._old_ddl = """
            PRAGMA foreign_keys = ON;
            PRAGMA journal_mode = WAL;
            PRAGMA synchronous = NORMAL;

            CREATE TABLE IF NOT EXISTS teams (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                name     TEXT NOT NULL UNIQUE,
                tricode1 TEXT,
                tricode2 TEXT,
                CHECK (name <> ''),
                CHECK (tricode1 IS NULL OR tricode1 <> ''),
                CHECK (tricode2 IS NULL OR tricode2 <> '')
            );

            -- Speed up lookups by code
            CREATE INDEX IF NOT EXISTS idx_teams_tricode1 ON teams(tricode1);
            CREATE INDEX IF NOT EXISTS idx_teams_tricode2 ON teams(tricode2);
            """
        self._old_upsert_sql = """
            INSERT INTO teams (name, tricode1, tricode2)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                tricode1 = excluded.tricode1,
                tricode2 = excluded.tricode2;
            """
        self._ddl = """
            PRAGMA foreign_keys = ON;
            PRAGMA journal_mode = WAL;
            PRAGMA synchronous = NORMAL;

            CREATE TABLE IF NOT EXISTS teams (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name       TEXT NOT NULL UNIQUE,
                conference      TEXT,
                conference_key  TEXT,
                division        TEXT,
                espn_key        TEXT,
                CHECK (team_name <> '')
            );
            """

        self._upsert_sql = """
            INSERT INTO teams (team_name, conference, conference_key, division, espn_key)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(team_name) DO UPDATE SET
                conference = excluded.conference,
                conference_key = excluded.conference_key,
                division = excluded.division,
                espn_key = excluded.espn_key;
            """
    def close(self):
        try:
            if self._conn:
                self._conn.close()
                self._conn = None
                print("Closed connection")
        except Exception as e:
            print(f"Error Exception: {e}")

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

    def normalize_codes(self, codes):
        if codes is None:
            return []
        if isinstance(codes, str):
            codes = [codes]
        # strip, uppercase, de-dupe while preserving order
        seen = set()
        out = []
        for c in codes:
            if c is None:
                continue
            cc = c.strip().upper()
            if cc and cc not in seen:
                seen.add(cc)
                out.append(cc)
        return out

    def pick_two(self, codes):
        # We only have two columns; keep first two if there are more
        c1 = codes[0] if len(codes) >= 1 else None
        c2 = codes[1] if len(codes) >= 2 else None
        return (c1, c2)

    def load_mapping(self, mapping):
        if self.table_exists("teams"):
            print("[info] Table 'teams' already exists. Skipping data load.")
            return False

        print("[info] Creating table and loading mapping...")
        self._cur.executescript(self._ddl)

        for team, codes in mapping.items():
            team_norm = (team or "").strip().lower()
            codes_norm = self.normalize_codes(codes)
            if len(codes_norm) > 2:
                print(f"[warn] {team}: has {len(codes_norm)} codes {codes_norm}; storing first two.")
            tri1, tri2 = self.pick_two(codes_norm)
            self._cur.execute(self._upsert_sql, (team_norm, tri1, tri2))

        self._conn.commit()
        return True

    def load_single_obj(self, obj: dict):
        team_name = obj.get("team_name", "").strip()
        if not team_name:
            print("[warn] Missing team_name, skipping.")
            return False

        print("[info] Creating table and loading dict if not already loaded...")
        self._cur.executescript(self._ddl)

        # Check if team_name already exists
        self._cur.execute("SELECT 1 FROM teams WHERE team_name = ?", (team_name,))
        if self._cur.fetchone():
            print(f"[info] Team '{team_name}' already exists. Skipping insert.")
            return False

        #if self.table_exists("teams"):
        #    print("[info] Table 'teams' already exists. Skipping data load.")
        #    return False
        print("[info] Creating table and loading dict...")
        self._cur.executescript(self._ddl)
        self._cur.execute(self._upsert_sql, (
            obj.get("team_name"),
            obj.get("conference"),
            obj.get("conference_key"),
            obj.get("division"),
            obj.get("espn_key")
        ))
        self._conn.commit()
        print(f"[info] upserted obj for {obj.get('team_name')}")
        return True


    def find_by_tricode(self, code: str):
        code = code.strip().upper()
        self._cur.execute(
            "SELECT id, name, tricode1, tricode2 FROM teams WHERE tricode1 = ? OR tricode2 = ?",
            (code, code),
        )
        return self._cur.fetchall()
    def select_print_all(self):
        self._cur.execute("""
            SELECT id, team_name, conference, conference_key, division, espn_key
            FROM teams
            ORDER BY team_name;
        """)
        rows = self._cur.fetchall()
        print(f"{'ID':<4} {'Team Name':<30} {'Conference':<20} {'Key':<6} {'Division':<6} {'ESPN Key':<10}")
        print("-" * 90)
        for row in rows:
            id_, team_name, conference, conf_key, division, espn_key = row
            print(f"{id_:<4} {team_name:<30} {conference or '-':<20} {conf_key or '-':<6} {division or '-':<6} {espn_key or '-':<10}")
        return rows


    def old_select_print_all(self):
        self._cur.execute("SELECT id, name, tricode1, tricode2 FROM teams ORDER BY name;")
        rows = self._cur.fetchall()
        for row in rows:
            print(row)   # each row is a tuple (id, name, tricode1, tricode2)
        return rows



if __name__=="__main__":
    print("Creating connection")
    db_file_path = "./new_database.db"
    input_json = "./updated_fbs_cfb_teams.json"
    conn = sqlite3.connect(db_file_path)
    db = CfbTeamDb(conn)
    with open(input_json, "r") as jsonfile:
        data = json.load(jsonfile)
        for k,v in data.items():
            data_obj = v
            data_obj["team_name"] = k
            db.load_single_obj(data_obj)
    #not_is_loaded = db.load_mapping(cfb_tricodes)
    db.select_print_all()
    db.close()

