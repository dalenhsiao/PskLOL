from SqlDB import SqlDB
import psycopg2
import psycopg2.extras as extras


class Operations(SqlDB):
    def __init__(self, user, host, password, db_name):
        """
        SqlDB class takes in sql server user name, host and password
        when Operations class is called, it connects to the sql server with
        the given credentials.
        (ex. Operations(user="user", host="host", password="password"))
        """
        # initialize SqlDB class
        super().__init__(user, host, password, db_name)

    def create_table(self, table_name, table_queries):
        """Create a table in the PostgreSQL database."""
        # if table_queries is None:
        #     if table_name is None:
        #         table_name = 
            # table_queries = self.generate_create_table_queries(df, table_name)
        self.table_name = table_name
        self.cur.execute(table_queries)
        self.conn.commit()
        print("Table created successfully")

    def insert_data(self, data):
        """Insert data into a table."""
        # self.cur.execute(insert_queries, data)
        # self.conn.commit()
        # print("Data inserted successfully")
        """Insert data from a DataFrame into a table."""
        # Create a list of tuples from the DataFrame values
        tuples = [tuple(x) for x in data.to_numpy()]
        
        # Get the column names from the DataFrame
        cols = ','.join(list(data.columns))
        
        # SQL query to execute
        query = f"INSERT INTO {self.table_name}({cols}) VALUES %s"
        
        try:
            extras.execute_values(self.cur, query, tuples)
            self.conn.commit()
            print("Data inserted successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            self.conn.rollback()
            return 1
        return 0
