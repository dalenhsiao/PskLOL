from .SqlDB import SqlDB
from typing import List, Optional


class SqlCommandList:
    def __init__(self, queries: Optional[List[str]] = None):
        # Assert that an instance of SqlDB exists
        assert SqlDB._instance is not None, "An instance of SqlDB must be created before creating SqlCommandList"

        self.db = SqlDB._instance
        self.queries = []
        if queries is not None:
            self.queries = queries

    def append(self, query):
        """Add a single SQL query to the list."""
        self.queries.append(query)

    def insert(self, index, query):
        """Insert a single SQL query at a specific index in the list."""
        self.queries.insert(index, query)

    # def add_queries(self, queries):
    #     """Add multiple SQL queries to the list."""
    #     if not hasattr(queries, '__iter__'):
    #         raise ValueError("Input should be an iterable containing SQL queries.")
    #     self.queries.extend(queries)

    def execute_queries(self):
        """Execute all SQL queries in the list sequentially and commit all at once."""
        try:
            for query in self.queries:
                self.execute_query(query)
            self.db.conn.commit()
            print("All queries executed and committed successfully.")
        except Exception as e:
            self.db.conn.rollback()
            print(f"Error executing queries, rolling back. Error: {e}")

    def execute_query(self, query):
        """Execute a single SQL query without committing."""
        try:
            self.db.cur.execute(query)
            print(f"Executed query: {query}")
        except Exception as e:
            print(f"Error executing query: {query}\n{e}")

    def __getitem__(self, index):
        return self.queries[index]

    def __setitem__(self, index, value):
        self.queries[index] = value

    def __delitem__(self, index):
        del self.queries[index]

    def __len__(self):
        return len(self.queries)

    def pop(self, index=-1):
        """Remove and return the query at the given index."""
        return self.queries.pop(index)

    def __iter__(self):
        return iter(self.queries)


if __name__ == "__main__":
    # Initialize SqlDB
    from omegaconf import OmegaConf

    config = OmegaConf.load("sqldb_configurations.yaml")
    db = SqlDB(user=config.user, host=config.host, password=config.pw, db_name=config.db_name)
    # import pdb ; pdb.set_trace()

    # Initialize SqlCommandList with some queries
    queries = [
        "CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));",
        "INSERT INTO test_table (name) VALUES ('Alice');",
        "INSERT INTO test_table (name) VALUES ('Bob');"
    ]
    sql_command_list = SqlCommandList(queries)

    # Add another query
    sql_command_list.append("INSERT INTO test_table (name) VALUES ('Charlie');")

    # Insert a query at a specific index
    sql_command_list.insert(1, "INSERT INTO test_table (name) VALUES ('David');")

    # Execute all queries
    sql_command_list.execute_queries()

    # Access a query by index
    print(sql_command_list[1])

    # Modify a query by index
    sql_command_list[1] = "INSERT INTO test_table (name) VALUES ('Edward');"

    # Delete a query by index
    del sql_command_list[2]

    # Pop a query
    popped_query = sql_command_list.pop()
    print(f"Popped query: {popped_query}")

    # Iterate over queries
    for query in sql_command_list:
        print(query)

    # Close the database connection
    db.close()
