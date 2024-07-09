import pytest
from psycopg2 import sql
from unittest.mock import patch, MagicMock
from PskLOL.SqlDB import SqlDB


# Fixture to set up the SqlDB instance
@pytest.fixture  # help to setup temperarily testing instance
def sql_db():
    with patch("PskLOL.SqlDB.psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        # Instantiate SqlDB
        db = SqlDB(
            user="test_user",
            host="test_host",
            password="test_password",
            db_name="test_db",
        )

        yield db

        # Teardown
        db.close()


# Test the creation of the database
def test_create_db(sql_db):
    sql_db._create_db()
    print(sql_db.cur.execute.call_args_list)  # Print all calls made to execute
    expected_query = sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s")
    expected_params = ["test_db"]
    sql_db.cur.execute.assert_any_call(expected_query, expected_params)
    assert sql_db.cur.execute.call_count >= 1


# Test the connection to the database
def test_connect(sql_db):
    sql_db._connect()
    sql_db.cur.execute.assert_called()


# Test the commit function
def test_commit(sql_db):
    sql_db.commit()
    sql_db.conn.commit.assert_called_once()


# # Test the Operations class
# def test_operations():
#     with patch('your_module.psycopg2.connect') as mock_connect:
#         mock_conn = MagicMock()
#         mock_cur = MagicMock()
#         mock_connect.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur

#         operations = Operations(user='test_user', host='test_host', password='test_password', db_name='test_db')

#         operations.perform_operation()
#         operations.cur.execute.assert_called_with("SELECT NOW()")
#         operations.cur.fetchone.assert_called_once()

#         operations.commit()
#         operations.conn.commit.assert_called_once()

#         operations.close()
#         operations.cur.close.assert_called_once()
#         operations.conn.close.assert_called_once()
