import pytest
from psycopg2 import sql
from unittest.mock import patch, MagicMock, call
from PskLOL.SqlDB import SqlDB
from PskLOL.SqlCommandList import SqlCommandList


@pytest.fixture
def sql_db():
    with patch('PskLOL.SqlDB.psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        # yield mock_conn, mock_cur  # setup mock connections back to test function
        # code here runs after the test is completed, tearing down the mock connections
        db = SqlDB(user='user', host='localhost', password='password', db_name='test_db')
        yield db

        print("Tearing down mock_db fixture")
        db.close()


def test_sql_command_list(sql_db):
    # Initialize SqlDB
    sql_db._connect()

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

    # Verify that all queries were executed
    expected_queries = [
        "CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));",
        "INSERT INTO test_table (name) VALUES ('David');",
        "INSERT INTO test_table (name) VALUES ('Alice');",
        "INSERT INTO test_table (name) VALUES ('Bob');",
        "INSERT INTO test_table (name) VALUES ('Charlie');"
    ]
    answer_queries = [
        "CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));",
        "INSERT INTO test_table (name) VALUES ('Edward');",
        "INSERT INTO test_table (name) VALUES ('Alice');",
        "INSERT INTO test_table (name) VALUES ('Bob');",
    ]
    # mock call the execution
    calls = [call.execute(query) for query in expected_queries]
    sql_db.cur.execute.assert_has_calls(calls, any_order=False)

    # Verify commit was called
    sql_db.conn.commit.assert_called_once()

    i = 0
    # Access a query by index
    assert sql_command_list[1] == "INSERT INTO test_table (name) VALUES ('David');"
    i += 1
    print("pass %d" % i)

    # Modify a query by index
    sql_command_list[1] = "INSERT INTO test_table (name) VALUES ('Edward');"
    assert sql_command_list[1] == "INSERT INTO test_table (name) VALUES ('Edward');"
    i += 1
    print("pass %d" % i)

    # Delete a query by index
    del sql_command_list[2]
    assert len(sql_command_list) == 4
    i += 1
    print("pass %d" % i)

    # Pop a query
    popped_query = sql_command_list.pop()
    assert popped_query is not None, f"actual popped : {popped_query}"
    assert len(sql_command_list) == 3
    i += 1
    print("pass %d" % i)

    # Iterate over queries
    for query in sql_command_list:
        assert query in answer_queries
    i += 1
    print("pass %d" % i)
