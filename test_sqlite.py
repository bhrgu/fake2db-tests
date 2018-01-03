from faker import Factory
import os
import pytest
import sqlite3
from conftest import simple_expected_tables, fake2db_minversion

testdb_name = os.environ.get('ENV_DBNAME') + '.db'

@pytest.fixture(scope="module")
def db_cursor(request):

    cnx = sqlite3.connect(testdb_name)
    cursor = cnx.cursor()

    def teardown():

        print("\nSQLite connection tearing down...\n")
        cnx.close()

    request.addfinalizer(teardown)
    return cursor


###### CUSTOM DB TESTS WITH DB NAME GIVEN ######


@pytest.mark.CUSTOM_WITH_NAME
def test_sqlite_custom_db_exists():

	assert os.path.exists(testdb_name) == True


@pytest.mark.CUSTOM_WITH_NAME
def test_sqlite_custom_table_exists(db_cursor):

    query = ("SELECT COUNT(NAME) FROM SQLITE_MASTER WHERE NAME='custom';")
    db_cursor.execute(query)
    result_set = db_cursor.fetchall()
    assert result_set[0][0] == 1


@pytest.mark.CUSTOM_WITH_NAME
def test_sqlite_custom_table_columns(db_cursor, custom_ecl):

    expected_columns_list = custom_ecl
    query = ("PRAGMA table_info(custom);")
    db_cursor.execute(query)
    result_set = db_cursor.fetchall()
    result_columns_list = list(map(lambda x: x[1], result_set))
    assert result_columns_list == expected_columns_list


@pytest.mark.CUSTOM_WITH_NAME
def test_sqlite_custom_table_row_count(db_cursor):

    query = ("SELECT COUNT(*) FROM custom;")
    db_cursor.execute(query)
    assert db_cursor.fetchall()[0][0] == 1


@pytest.mark.CUSTOM_WITH_NAME
def test_sqlite_custom_table_data(db_cursor):

    fake = Factory.create()
    fake.seed(1)
    name, date, country = fake.name(), fake.date(), fake.country()
    query = ("SELECT * FROM custom;")
    db_cursor.execute(query)
    result_set = db_cursor.fetchall()
    assert result_set[0][1] == name
    assert result_set[0][2] == date
    assert result_set[0][3] == country


###### SIMPLE DB TESTS WITH DB NAME GIVEN ######


@fake2db_minversion
@pytest.mark.SIMPLE_WITH_NAME
def test_sqlite_simple_db_exists():

	assert os.path.exists(testdb_name) == True


@fake2db_minversion
@pytest.mark.SIMPLE_WITH_NAME
def test_sqlite_simple_db_tables_exists(db_cursor, simple_etl):

    expected_tables_list = simple_etl
    query = ("SELECT NAME FROM SQLITE_MASTER WHERE TYPE='table' ORDER BY NAME;")
    db_cursor.execute(query)
    result_set = db_cursor.fetchall()
    tables_list = [x for y in result_set for x in y]
    assert tables_list == expected_tables_list


@fake2db_minversion
@pytest.mark.SIMPLE_WITH_NAME
def test_sqlite_simple_table_columns(db_cursor, simple_db_table_columns):

    (table_name, expected_columns_list) = simple_db_table_columns

    query = ("PRAGMA table_info({table});".format(table=table_name))
    db_cursor.execute(query)
    result_set = db_cursor.fetchall()
    result_columns_list = list(map(lambda x: x[1], result_set))
    assert result_columns_list == expected_columns_list


@fake2db_minversion
@pytest.mark.SIMPLE_WITH_NAME
@pytest.mark.parametrize("table", simple_expected_tables)
def test_sqlite_simple_table_row_count(db_cursor, table):

    table_name = table
    query = (
        "SELECT COUNT(*) FROM {table};".format(table=table_name))
    db_cursor.execute(query)
    assert db_cursor.fetchall()[0][0] == 1


@fake2db_minversion
@pytest.mark.SIMPLE_WITH_NAME
def test_sqlite_simple_table_data(db_cursor):

    table_name = 'simple_registration'

    fake = Factory.create()
    fake.seed(1)
    expected_value = fake.safe_email()

    query = ("SELECT email FROM {table};".format(table=table_name))
    db_cursor.execute(query)
    result_set = db_cursor.fetchall()
    assert result_set[0][0] == expected_value
