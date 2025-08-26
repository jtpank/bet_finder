import csv
import json
import difflib

# --- Load and combine FBS + FCS team metadata ---
with open("updated_fbs_cfb_teams.json", "r", encoding="utf-8") as fbs_file:
    fbs_teams = json.load(fbs_file)

with open("updated_fcs_cfb_teams.json", "r", encoding="utf-8") as fcs_file:
    fcs_teams = json.load(fcs_file)

# Combine both dictionaries into one
combined_teams = {**fbs_teams, **fcs_teams}

# Normalize keys for fuzzy matching
normalized_keys = {k.strip().lower(): k for k in combined_teams.keys()}

# --- Extract unique team names from CSV ---
csv_teams = set()
with open("cfb_db_2024.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        team = row.get("Team")
        if team:
            csv_teams.add(team.strip().lower())

# --- Match CSV teams to closest combined JSON key ---
team_matches = {}

for team in sorted(csv_teams):
    match = difflib.get_close_matches(team, normalized_keys.keys(), n=1, cutoff=0.6)
    if match:
        matched_name = normalized_keys[match[0]]
        team_matches[team] = matched_name
    else:
        team_matches[team] = ""

# --- Output to single JSON file ---
with open("team_matches_combined.json", "w", encoding="utf-8") as outfile:
    json.dump(team_matches, outfile, indent=2)

print("[✓] Done! Results written to 'team_matches_combined.json'")