import psycopg2


class SqlDB():
    def __init__(self, user, host, password, db_name) -> None:
        self.user = user
        self.host = host
        self.pw = password
        self.conn = None
        self.cur = None
        self.db_name = db_name
        self.create_db()

    # when called it connect to sql database
    def __call__(self):
        conn, cur = self.create_db(self.db_name)
        return conn, cur

    def create_db(self):
        self.conn = psycopg2.connect(f"host={self.host} dbname=postgres user={self.user} password={self.pw}")
        self.conn.set_session(autocommit=True)
        self.cur = self.conn.cursor()
        # # create a database with UTF8 encoding
        # cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid)\
        #             FROM pg_stat_activity\
        #             WHERE pg_stat_activity.datname = '{self.db_name}'\
        #                 AND pid <> pg_backend_pid();")
        # print("Disconnedted all existing sessions for the database")
        # cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
        # cur.execute(f"CREATE DATABASE {self.db_name} WITH ENCODING 'utf8' TEMPLATE template0")
        # Check if the database exists
        self.cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{self.db_name}'")
        exists = self.cur.fetchone()

        if not exists:
            # Database does not exist, create it
            self.cur.execute(f"CREATE DATABASE {self.db_name} WITH ENCODING 'utf8' TEMPLATE template0")
            print("Database created.")
        else:
            print("Database already exists.")
        # close connection to default database
        self.conn.close()
        self.cur.close()
        # connect to sparkify database
        self.conn = psycopg2.connect(f"host={self.host} dbname={self.db_name} user={self.user} password={self.pw}")
        self.cur = self.conn.cursor()
        print("SQL DB connected")

    def close(self):
        self.conn.close()
        self.cur.close()
