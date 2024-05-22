import requests
from pathlib import Path
import pandas as pd
import psycopg2
from SqlOperations import Operations


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


# class SqlDB():
#     def __init__(self, user, host, password) -> None:
#         self.user = user
#         self.host = host
#         self.pw = password

#     # when called it connect to sql database
#     def __call__(self, db_name):
#         conn, cur = self.create_db(db_name)
#         return conn, cur

#     def create_db(self, db_name):
#         conn = psycopg2.connect(f"host={self.host} dbname=postgres user={self.user} password={self.pw}")
#         conn.set_session(autocommit=True)
#         cur = conn.cursor()
#         # create a database with UTF8 encoding
#         cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid)\
#                     FROM pg_stat_activity\
#                     WHERE pg_stat_activity.datname = '{db_name}'\
#                         AND pid <> pg_backend_pid();")
#         print("Disconnedted all existing sessions for the database")
#         cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
#         cur.execute(f"CREATE DATABASE {db_name} WITH ENCODING 'utf8' TEMPLATE template0")
#         print("DB created")
#         # close connection to default database
#         conn.close()
#         # connect to sparkify database
#         conn = psycopg2.connect(f"host={self.host} dbname={db_name} user={self.user} password={self.pw}")
#         cur = conn.cursor()
#         return conn, cur
    
#     def creare_table(self, table_name, columns):
#         query = f"CREATE TABLE {table_name} ({columns})"
#         self.cur.execute(query)
#         self.conn.commit()
#         print("Table created")

# class DB_connector():
#     def __init__(self, db_name: str, *sqlconfigs):
#         self.db_name = db_name
#         user, host, password = sqlconfigs
#         self.ops = Operations(user, host, password, self.db_name)

#     def insert_data(self, data, table_name):
#         for i, row in data.iterrows():
#             self.cur.execute(f"INSERT INTO {table_name} VALUES {tuple(row)}")
#             self.conn.commit()
#         print("Data inserted")
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
