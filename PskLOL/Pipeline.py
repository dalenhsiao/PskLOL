from SqlOperations import Operations
from omegaconf import OmegaConf

config = OmegaConf.load("sqldb_configurations.yaml")


class Pipeline:
    def __init__(self):
        self.sqlops = Operations(
            user=config.user,
            host=config.host,
            password=config.password,
            db_name=config.db_name
        )
        self.search_query = None # initialize sql query

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Each pipeline stage must implement the '__call__' method.")
