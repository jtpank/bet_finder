from utilities import OddsDataFetcher, SportsEnum

def main():
    print("Hello from download-odds-api-data!")
    df = OddsDataFetcher(version=4) #odds api version 4
    df.get_events(SportsEnum.NFL)


if __name__ == "__main__":
    main()
