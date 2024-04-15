import PskLOL as lol
import pandas as pd
from PskLOL._updatedb import DB_connector


def test_fetch_data():
    result = lol._updatedb.fetch_data(
        "carnegie mellon university"
    )
    assert isinstance(result, pd.DataFrame)


def test_fetch_local_db():
    db = DB_connector('PskLOL/_db/data.csv')
    assert db.read_from_csv() is not {}


def test_update_db():
    db = DB_connector('PskLOL/_db/data.csv')
    assert db.update_data(db.data)


def test_get_data():
    db = DB_connector('PskLOL/_db/data.csv')
    assert isinstance(db.get_data(), pd.DataFrame)
