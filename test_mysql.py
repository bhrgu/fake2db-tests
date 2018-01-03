from faker import Factory
import mysql.connector
import os
import pytest
from conftest import simple_expected_tables, fake2db_minversion

hostname = os.environ.get('ENV_HOST')
instance_port = int(os.environ.get('ENV_PORT'))
mysql_user = os.environ.get('ENV_USER')
mysql_pass = os.environ.get('ENV_PASS')
testdb_name = os.environ.get('ENV_DBNAME')


@pytest.fixture(scope="module")
def db_cursor(request):

    cnx = mysql.connector.connect(user=mysql_user, password=mysql_pass,
                                  host=hostname, port=instance_port)
    cursor = cnx.cursor()

    def teardown():

        print("\nMySQL connection tearing down...\n")
        query = ("DROP DATABASE IF EXISTS {database};".format(
            database=testdb_name))
        cursor.execute(query)
        cnx.close()

    request.addfinalizer(teardown)
    return cursor


###### CUSTOM DB TESTS W/O DB NAME GIVEN ######

@pytest.mark.CUSTOM_WITHOUT_NAME
def test_mysql_custom_random_name_db_exists(db_cursor):

    query = (
        "SELECT TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='custom';")
    db_cursor.execute(query)
    result = db_cursor.fetchall()[0][0]

    global testdb_name
    testdb_name = result  # for correct dropping the random named DB after testrun

    assert db_cursor.rowcount == 1
    assert result[:6] == 'mysql_'
    assert len(result) == 14


@pytest.mark.CUSTOM_WITHOUT_NAME
def test_mysql_custom_random_name_columns(db_cursor, custom_ecl):

    expected_columns_list = custom_ecl
    query = (
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'custom';")
    db_cursor.execute(query)
    result_set = db_cursor.fetchall()
    result_columns_list = [x for y in result_set for x in y]
    assert result_columns_list == expected_columns_list


###### CUSTOM DB TESTS WITH DB NAME GIVEN ######

@pytest.mark.CUSTOM_WITH_NAME
def test_mysql_custom_db_exists(db_cursor):

    query = (
        "SELECT COUNT(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s;")
    db_cursor.execute(query, (testdb_name,))
    db_cursor.fetchall()
    assert db_cursor.rowcount == 1


@pytest.mark.CUSTOM_WITH_NAME
def test_mysql_custom_table_exists(db_cursor):

    query = ("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=%s;")
    db_cursor.execute(query, (testdb_name,))
    result_set = db_cursor.fetchall()
    assert db_cursor.rowcount == 1
    assert result_set[0][0] == 'custom'


@pytest.mark.CUSTOM_WITH_NAME
def test_mysql_custom_table_columns(db_cursor, custom_ecl):

    expected_columns_list = custom_ecl
    query = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;")
    db_cursor.execute(query, (testdb_name, 'custom'))
    result_set = db_cursor.fetchall()
    result_columns_list = [x for y in result_set for x in y]
    assert result_columns_list == expected_columns_list


@pytest.mark.CUSTOM_WITH_NAME
def test_mysql_custom_table_row_count(db_cursor):

    table_name = testdb_name + '.custom'
    query = ("SELECT COUNT(*) FROM {table};".format(table=table_name))
    db_cursor.execute(query)
    assert db_cursor.fetchall()[0][0] == 1


@pytest.mark.CUSTOM_WITH_NAME
def test_mysql_custom_table_data(db_cursor):

    table_name = testdb_name + '.custom'
    fake = Factory.create()
    fake.seed(1)
    name, date, country = fake.name(), fake.date(), fake.country()
    query = ("SELECT * FROM {table};".format(table=table_name))
    db_cursor.execute(query)
    result_set = db_cursor.fetchall()
    assert result_set[0][1] == name
    assert result_set[0][2] == date
    assert result_set[0][3] == country


###### SIMPLE DB TESTS W/O DB NAME GIVEN ######

@pytest.mark.SIMPLE_WITHOUT_NAME
def test_mysql_simple_random_name_db_exists(db_cursor):

    query = (
        "SELECT TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='simple_registration';")
    db_cursor.execute(query)
    result = db_cursor.fetchall()[0][0]

    global testdb_name
    testdb_name = result  # for correct dropping the random named DB after testrun

    assert db_cursor.rowcount == 1
    assert result[:6] == 'mysql_'
    assert len(result) == 14


@pytest.mark.SIMPLE_WITHOUT_NAME
def test_mysql_simple_random_name_table_columns(db_cursor, simple_db_table_columns):

    (table_name, expected_columns_list) = simple_db_table_columns

    query = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;")
    db_cursor.execute(query, (testdb_name, table_name,))
    result_set = db_cursor.fetchall()
    result_columns_list = [x for y in result_set for x in y]
    assert result_columns_list == expected_columns_list


###### SIMPLE DB TESTS WITH DB NAME GIVEN ######

@fake2db_minversion
@pytest.mark.SIMPLE_WITH_NAME
def test_mysql_simple_db_exists(db_cursor):

    query = (
        "SELECT COUNT(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s;")
    db_cursor.execute(query, (testdb_name,))
    db_cursor.fetchall()
    assert db_cursor.rowcount == 1


@fake2db_minversion
@pytest.mark.SIMPLE_WITH_NAME
def test_mysql_simple_db_tables_exists(db_cursor, simple_etl):

    expected_tables_list = simple_etl
    query = ("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=%s;")
    db_cursor.execute(query, (testdb_name,))
    result_set = db_cursor.fetchall()
    tables_list = sorted([x for y in result_set for x in y])
    assert db_cursor.rowcount == 5
    assert tables_list == expected_tables_list


@fake2db_minversion
@pytest.mark.SIMPLE_WITH_NAME
def test_mysql_simple_table_columns(db_cursor, simple_db_table_columns):

    (table_name, expected_columns_list) = simple_db_table_columns

    query = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;")
    db_cursor.execute(query, (testdb_name, table_name,))
    result_set = db_cursor.fetchall()
    result_columns_list = [x for y in result_set for x in y]
    assert result_columns_list == expected_columns_list


@fake2db_minversion
@pytest.mark.SIMPLE_WITH_NAME
@pytest.mark.parametrize("table", simple_expected_tables)
def test_mysql_simple_table_row_count(db_cursor, table):

    table_name = testdb_name + '.' + table
    query = (
        "SELECT COUNT(*) FROM {table};".format(table=table_name))
    db_cursor.execute(query)
    assert db_cursor.fetchall()[0][0] == 1


@fake2db_minversion
@pytest.mark.SIMPLE_WITH_NAME
def test_mysql_simple_table_data(db_cursor):

    table_name = testdb_name + '.simple_registration'

    fake = Factory.create()
    fake.seed(1)
    expected_value = fake.safe_email()

    query = ("SELECT email FROM {table};".format(table=table_name))
    db_cursor.execute(query)
    result_set = db_cursor.fetchall()
    assert result_set[0][0] == expected_value
