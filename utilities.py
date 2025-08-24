import requests
from datetime import datetime
from enum import Enum
from dotenv import dotenv_values

config = dotenv_values(".env")

class SportsEnum(Enum):
    NFL="americanfootball_nfl"

class OddsDataFetcher():
    def __init__(self, version: int):
        assert version == 4, "Can only handle Odds API V4!"
        self.base_url = "https://api.the-odds-api.com/v4"

    # helper to wrap requests
    def make_request(self, url: str):
        print(f"Attempting get request to {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"Succesfully received data! Type: {type(data)}")
                return data
        except Exception as e:
            print(f"Exception {e}")
            return None

    # handle types
    def process_odds_api_data(self, data):
        print(type(data))
        if isinstance(data, list):
            self.process_list_data(data)
        if isinstance(data, dict):
            self.process_dict_data(data)

    # helper to abstractlly process json data
    def process_dict_data(self, data: dict):
        print("Process dict data")

    def process_list_data(self, data: list):
        print("Process list data")

    #Request sport events
    def get_events(self, sport: SportsEnum):
        url = (
                f"{self.base_url}/sports/{sport.value}/events"
                f"?apiKey={config.get('API_KEY')}"
        )
        data = self.make_request(url)
        if not data:
            print("Could not process None data in get_events")
            return
        print("Processing data!")
        self.process_odds_api_data(data)


def main():
    print("utilites.py")

if __name__=="__main__":
    main()
