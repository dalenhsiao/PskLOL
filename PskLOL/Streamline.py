from Pipeline import Pipeline
import pandas as pd
import requests


# fectching data from openalex api
class producer(Pipeline):
    def __init__(self):
        super().__init__()

    def __call__(
        self,
        search_query: str,
        source: str = "https://api.openalex.org/institutions"
    ):
        self.search_query = search_query
        data = self.fetch_data(self.search_query, source)
        return data

    def fetch_data(
        self,
        query: str,
        source: str
    ):
        """

        Args:
            source (_type_): openalex api url

        Returns:
            data (pd DataFrame): data from the openalex api
        """
        params = {"search": query}
        url = source
        response = requests.get(url, params=params) # input response is json file
        
        if response.status_code == 200:
            response = response.json()
            data = pd.json_normalize(response['results'])
            return data
        else:
            return -1


class consumer(Pipeline):
    def __init__(self):
        super().__init__()

    def __call__(self, data: pd.DataFrame, table_name: str = None, table_queries: str = None):
        if table_queries is None:
            table_queries = self.generate_create_table_queries(
                data,
                table_name
            )
            print(table_queries)
        self.sqlops.create_table(table_name, table_queries)
        self.sqlops.insert_data(data)
        print("Table created successfully")
        return data

    def generate_create_table_queries(self, df, table_name):
        if table_name is None:
            table_name = self.search_query
        cols = []
        for col_name, dtype in zip(df.columns, df.dtypes):
            if dtype == 'int64':
                sql_dtype = 'INTEGER'
            elif dtype == 'float64':
                sql_dtype = 'FLOAT'
            elif dtype == 'object':
                sql_dtype = 'TEXT'
            else:
                sql_dtype = 'TEXT'
            cols.append(f"{col_name} {sql_dtype}")
        cols_str = ", ".join(cols)
        create_table_statement = f"CREATE TABLE {table_name} ({cols_str});"
        return create_table_statement


if __name__ == "__main__":
    producer = producer()
    data = producer("carnegie mellon university")
    print(data)
    consumer = consumer()
    data = consumer(data)
    
    from pdb import set_trace; set_trace()
    # consumer = consumer()
    # consumer(data, "university")
