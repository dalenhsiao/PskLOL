import psycopg2
from psycopg2 import sql
from typing import Union


class SqlDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SqlDB, cls).__new__(cls)
        return cls._instance

    def __init__(self, user, host, password, db_name):
        if not hasattr(self, 'initialized'):  # To prevent reinitialization
            self.user = user
            self.host = host
            self.pw = password
            self.db_name = db_name
            self.conn = None
            self.cur = None
            self._create_db()
            self._connect()
            self.initialized = True

    # # when called it connect to sql database
    # def __call__(self):
    #     self.create_db(self.db_name)

    def _create_db(self):
        conn = None
        cur = None
        try:
            # Connect to the default database to create the new database
            conn = psycopg2.connect(
                f"host={self.host} dbname=postgres user={self.user} password={self.pw}"
            )
            conn.set_session(autocommit=True)
            cur = conn.cursor()
            # Check if the database exists
            cur.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [self.db_name]
            )
            exists = cur.fetchone()
            if not exists:
                # Database does not exist, create it
                cur.execute(
                    sql.SQL(
                        "CREATE DATABASE {} WITH ENCODING 'utf8' TEMPLATE template0"
                    ).format(sql.Identifier(self.db_name))
                )
                print(f"Database '{self.db_name}' created.")
            else:
                print(f"Database '{self.db_name}' already exists.")
        except Exception as e:
            print(f"Error creating database '{self.db_name}': {e}")
            # return 1
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
            # return 0
        # self.conn = psycopg2.connect(f"host={self.host} dbname=postgres user={self.user} password={self.pw}")
        # self.conn.set_session(autocommit=True)
        # self.cur = self.conn.cursor()
        # # # create a database with UTF8 encoding
        # # cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid)\
        # #             FROM pg_stat_activity\
        # #             WHERE pg_stat_activity.datname = '{self.db_name}'\
        # #                 AND pid <> pg_backend_pid();")
        # # print("Disconnedted all existing sessions for the database")
        # # cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
        # # cur.execute(f"CREATE DATABASE {self.db_name} WITH ENCODING 'utf8' TEMPLATE template0")
        # # Check if the database exists
        # self.cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{self.db_name}'")
        # exists = self.cur.fetchone()

        # if not exists:
        #     # Database does not exist, create it
        #     self.cur.execute(f"CREATE DATABASE {self.db_name} WITH ENCODING 'utf8' TEMPLATE template0")
        #     print("Database created.")
        # else:
        #     print("Database already exists.")
        # # close connection to default database
        # self.conn.close()
        # self.cur.close()
        # # # connect to sparkify database
        # # self.conn = psycopg2.connect(f"host={self.host} dbname={self.db_name} user={self.user} password={self.pw}")
        # # self.cur = self.conn.cursor()
        # # print("SQL DB connected")

    def _connect(self):
        try:
            # Connect to the specified database
            self.conn = psycopg2.connect(
                f"host={self.host} dbname={self.db_name} user={self.user} password={self.pw}"
            )
            self.cur = self.conn.cursor()
            print("SQL DB connected")
            # return 0
        except Exception as e:
            print(f"Error connecting to database: {e}")
            # return 1

    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            print(f"Error committing transaction: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
        if self.cur:
            self.cur.close()


if __name__ == "__main__":
    from omegaconf import OmegaConf

    config = OmegaConf.load("sqldb_configurations.yaml")
    db = SqlDB(
        user=config.user,
        host=config.host,
        password=config.password,
        db_name=config.db_name,
    )
    print(db.conn)
    db.close()
