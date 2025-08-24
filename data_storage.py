from dotenv import dotenv_values
from pathlib import Path
config = dotenv_values(".env")

class DataStorage():
    def __init__(self):
        self.base_dir = Path(config.get("DATA_STORAGE_PATH"))

def main():
    print("Data Storage Helper")
if __name__=="__main__":
    main()
