import requests
from enum import Enum
from typing import Optional
from pathlib import Path
import json

#/home/justin/Desktop/000-github/download-odds-api-data/bovada-data/ncaaf#2025#regular_season
# https://sports.core.api.espn.com/v2/sports/football/leagues/college-football/seasons/2025/types/2/weeks/1/events?lang=en&region=us&page=4

class EspnSport(Enum):
    NCAAF="football/leagues/college-football"

class EspnSeason(Enum):
    PRE=1
    REG=2
    POST=3

class EspnApi():
    def __init__(self, debug=False):
        self.data_storage_path = Path("/home/justin/Desktop/sports#2025#datastore/ncaaf#2025")
        self.base_url = "https://sports.core.api.espn.com/v2/sports"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json, text/plain, */*",
            # (maybe?) "Referer": "https://www.espn.com/",
        }

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

    def parse_request_metadata(self, data: dict):
        # and pages / page count data
        # assert metadata == input data for sanity
        count = data["count"]
        page_index = data["pageIndex"]
        page_count = data["pageCount"]
        page_data = {
            "count": count,
            "page_count": page_count,
            "page_index": page_index
        }
        return page_data

    def get_all_event_data(self, sport: EspnSport, season: int,
                           season_type: EspnSeason, week: int,
                           page_index: Optional[int] = 1):
        # 1. make the first request
        # 2. get the first request metadata
        # 3. iterate over all the pages and get the events
        all_events_array = []
        # make the events url
        url_start = (f"{self.base_url}"
                f"/{sport.value}"
                f"/seasons/{season}"
                f"/types/{season_type.value}"
                f"/weeks/{week}"
                f"/events"
        )
        url_end = f"?lang=en&region=us&page={page_index}"
        url = url_start + url_end
        data = self.make_request(url)
        page_data = self.parse_request_metadata(data)
        all_events_array = self.parse_events_items(data)
        for idx in range(2, page_data["page_count"] + 1):
            url_end = f"?lang=en&region=us&page={idx}"
            url = url_start + url_end
            next_data = self.make_request(url)
            all_events_array.extend(self.parse_events_items(next_data))
        assert len(all_events_array) == page_data["count"], f"Page data count != events array, {page_data['count']} != {len(all_events_array)}"
        return all_events_array

    def parse_events_items(self, data: dict):
        output = []
        assert "items" in data.keys(), "No items array when parsing events items"
        items_array = data["items"]
        for event in items_array:
            output.append(event["$ref"])
        return output

    def get_data_from_event_urls(self, url_array: list, season: int, season_type: EspnSeason, week: int):
        espn_data_set = {}
        for url in url_array:
            data = self.make_request(url)
            keys_list = ["id", "date", "name", "shortName"]
            sub_data = {k: data[k] for k in keys_list if k in data}
            sub_data["season"] = season
            sub_data["season_type"] = season_type.value
            sub_data["week"] = week
            espn_data_set[data["id"]] = sub_data
        return espn_data_set

    def save_data_to_json(self, data_set: dict, espn_id_file: str):
        data_file_path = self.data_storage_path / espn_id_file
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

    def check_if_file_exists(self, espn_id_file: str):
        data_file_path = self.data_storage_path / espn_id_file
        return data_file_path.exists()


    def run(self, sport: EspnSport, season: int, season_type: EspnSeason, week:int, espn_id_file: str):
        if self.check_if_file_exists(espn_id_file):
            print(f"File: {espn_id_file} already exists!")
            return
        events_urls_array = self.get_all_event_data(sport, season, season_type, week)
        espn_data_set = self.get_data_from_event_urls(events_urls_array, season, season_type, week)
        self.save_data_to_json(espn_data_set, espn_id_file)



def main():
    ea = EspnApi()
    season = 2025
    sport = EspnSport.NCAAF
    season_type = EspnSeason.REG
    weeks = [i for i in range(1, 4)]
    for week in weeks:
        espn_id_file = f"espn#{season}#ids#week#{week}.json"
        ea.run(sport, season, season_type, week, espn_id_file)



if __name__=="__main__":
    main()



