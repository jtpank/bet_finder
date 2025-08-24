import requests
from datetime import datetime
from pathlib import Path
from typing import Optional
import json
from enum import Enum

class BovadaSports(Enum):
    NBASL="basketball/nba-summer-league"
    NCAAF="football/college-football"
class BovadaLive(Enum):
    LIVE="liveOnly=true"
    PRE="preMatchOnly=true"


class BovadaDataFetcher():
    def __init__(self, debug=False):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.bovada.lv/",
        }
        self.base_url = "https://www.bovada.lv/services/sports/event/coupon/events/A/description"
        self.debug = debug
        self.base_data_storage_path = Path("/home/justin/Desktop/sports#2025#datastore")
    def make_request(self, url: str):
        print(f"Attempting get request to {url}")
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                print(f"Received data! Type: {type(data)}")
                return data
        except Exception as e:
            print(f"Exception {e}")
            return None
    def save_data_to_json(self, data_set: dict, sub_dir: str, file_name: str):
        data_file_path = self.base_data_storage_path / sub_dir / file_name
        try:
            with open(data_file_path, 'w') as json_file:
                json.dump(data_set, json_file, indent=4)
            print(f"Succesfully wrote data to : {data_file_path}")
            return
        except FileNotFoundError:
            print(f"[Missing] File not found: {data_file_path}")
            return
        except json.JSONDecodeError:
            print(f"[Corrupt] Invalid JSON in file: {data_file_path}")
            return
        except Exception as e:
            print(f"[Error] Unexpected error with file {data_file_path}: {e}")
            return
    def parse_events(self, data: list, sport: BovadaSports,
                     bovada_type: BovadaLive, season: int, 
                     save_event_data: Optional[bool] = False):
        assert len(data) == 1, "Data array must be size 1"
        item = data[0]
        path_data = item["path"]
        events_array = item["events"]
        print(f"Events array is size {len(events_array)}")
        event_data_set = {}
        for event in events_array:
            id = event["id"]
            description = event["description"]
            start_time = datetime.fromtimestamp(int(event["startTime"]) / 1000)
            last_modified = datetime.fromtimestamp(int(event["lastModified"]) / 1000)
            display_groups_array = event["displayGroups"]
            keys_list = ["id", "description", "startTime", "lastModified"]
            sub_data = {k: event[k] for k in keys_list if k in event}
            sub_data["startTimeIso"] = start_time.isoformat()
            sub_data["lastModifiedIso"] = last_modified.isoformat()
            event_data_set[id] = sub_data
            if self.debug:
                print(f"id : {id}")
                print(f"description: {description}")
                print(f"start_time: {start_time}")
            self.parse_display_groups(display_groups_array)
        if save_event_data:
            bovada_event_file = f"bovada#{sport.name.lower()}#{season}#{bovada_type.name.lower()}.json"
            data_dir = f"{sport.name.lower()}#{season}"
            self.save_data_to_json(event_data_set, data_dir, bovada_event_file)

    def parse_display_groups(self, data: list):
        assert len(data) == 1, "Display groups array must be size 1"
        markets_array = data[0]["markets"]
        print(f"\tmarkets length: {len(markets_array)}")
        market_set = set()
        for market in markets_array:
            market_id = market["id"]
            market_description = market["description"]
            outcomes_array = market["outcomes"]
            if self.debug:
                print(f"\tmarket_id : {market_id}")
                print(f"\tmarket_description : {market_description}")
            if market_description not in market_set:
                market_set.add(market_description)
                self.parse_outcomes_array(outcomes_array)

    def parse_outcomes_array(self, data: list):
        print(f"\t\t outcomes len : {len(data)}")
        # Note: Bovada shows multiple e.g Moneylines / Totals for the same outcome 
        # so for simplicity (and from what ive seen) we choose the first one 
        # this is performed in the parse_display groups using the market_set
        for outcome in data:
            outcome_id = outcome["id"]
            outcome_description = outcome["description"]
            price = outcome["price"]
            price_decimal = price["decimal"]
            if self.debug:
                print(f"\t\t outcome_description : {outcome_description}")
                print(f"\t\t price_decimal : {price_decimal}")

    def run(self, sport: BovadaSports, live: BovadaLive, season: int):
        # TODO: make a generate url function?
        url = (f"{self.base_url}"
                f"/{sport.value}"
                f"?marketFilterId=def"
                f"&{live.value}"
                f"&eventsLimit=50"
                f"&lang=en"
        )
        data = self.make_request(url)
        print(len(data))
        self.parse_events(data, sport, live, season, save_event_data=True)

def test_fetch():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.bovada.lv/",
    }
    #url = "https://www.bovada.lv/services/sports/config/site"
    url = ("https://www.bovada.lv/services/sports/"
            "event/coupon/events/A/description/basketball/nba-summer-league"
            "?marketFilterId=def&liveOnly=true&eventsLimit=5000&lang=en"
            )
    # https://www.bovada.lv/services/sports/event/coupon/events/A/description/football?marketFilterId=def&preMatchOnly=true&eventsLimit=50&lang=en
    print(f"requesting url: {url}")
    response = requests.get(url, headers=headers)
    data = response.json()
    pretty_json = json.dumps(data, indent=2)
    for i in data:
        events = i["events"]
        for event in events:
            if event["id"] == "15517483":
                pretty_j = json.dumps(event, indent=2)
                print(pretty_j)
def test():
    path = "/home/justin/Desktop/000-github/download-odds-api-data/bovada-data/nba-summer.json"
    path2 = "/home/justin/Desktop/sports#2025#datastore/ncaaf#2025"
    with open(path, 'r') as f:
        data = json.load(f)
        for k, v in data.items():
            print(k)
        displayGroups = data['displayGroups']
        for group in displayGroups:
            markets = group['markets']
            for market in markets:
                print(market["description"])
                print(market["outcomes"])
def main():
    bdf = BovadaDataFetcher(debug=True)
    season = 2025
    sport = BovadaSports.NCAAF
    live = BovadaLive.PRE
    bdf.run(sport, live, season)

if __name__=="__main__":
    main()
