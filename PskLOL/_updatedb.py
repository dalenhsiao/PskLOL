import requests
from pathlib import Path
import pandas as pd


def fetch_data(query: str) -> dict:
    params = {"search": query}
    url = "https://api.openalex.org/institutions"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response = response.json()
        data = pd.json_normalize(response['results'])
        return data
    else:
        return -1


class DB_connector():
    def __init__(self, fp: str = None, debug=False):
        self.fp = Path(fp)
        self.debug = debug
        self.data = self.read_from_csv()

    def save_to_csv(self) -> None:
        self.data.to_csv(self.fp)

    def read_from_csv(self) -> dict:
        if self.fp.exists():
            self.data = pd.read_csv(self.fp)
            if self.debug:
                print("=====================================")
                print("Read from csv Complete")
            return self.data
        else:
            return {}  # return an empty dictionary

    def get_data(self):
        return self.data

    def update_data(self, data: pd.DataFrame) -> bool:
        self.data = pd.concat([pd.DataFrame(self.data), data])
        if self.debug:
            print("=====================================")
            print("Update Complete")
        return True


if __name__ == "__main__":
    # # autoupdate the local database
    # # Get the directory of the current script
    # current_dir = os.path.dirname(__file__)
    # # Construct the path to the '_db' directory
    # db_dir = os.path.join(current_dir, "_db")
    # # Ensure the '_db' directory exists
    # os.makedirs(db_dir, exist_ok=True)
    # # Specify the path to the 'institute_db.json' file
    # institute_path = os.path.join(db_dir, "institute_db.json")
    db = DB_connector('_db/institute_db.json')
    df = fetch_data('carnegie mellon university')
    print(df)
    db.update_data(df)
