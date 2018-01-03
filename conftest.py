import pytest
from fake2db import __version__

# Test data

simple_expected_tables = ['company', 'customer', 'detailed_registration', 'simple_registration', 'user_agent']

# Marks

fake2db_minversion = pytest.mark.skipif(__version__ < '0.5.4',
                                        reason="Not implemented in fake2db < 0.5.4")

# Fixtures


@pytest.fixture(scope="function", params=[
    ('expected_columns', ['id', 'name', 'date', 'country'])],
    ids=lambda param: param[0])
def custom_ecl(request):
    '''
    Custom database expected columns fixture
    '''
    return request.param[1]


@pytest.fixture(scope="function", params=[
    # ('expected_tables', ['company', 'customer', 'detailed_registration', 'simple_registration', 'user_agent'])],
    ('expected_tables', simple_expected_tables)],
    ids=lambda param: param[0])
def simple_etl(request):
    '''
    Simple database expected tables fixture
    '''
    return request.param[1]


@pytest.fixture(scope="function", params=[
    ("simple_registration", ['id', 'email', 'password']),
    ("detailed_registration", [
     'id', 'email', 'password', 'lastname', 'name', 'address', 'phone']),
    ("company", ['id', 'name', 'sdate', 'email', 'domain', 'city']),
    ("user_agent", ['id', 'ip', 'countrycode', 'useragent']),
    ("customer", ['id', 'name', 'lastname', 'address', 'country', 'city', 'registry_date', 'birthdate', 'email', 'phone_number', 'locale'])],
    ids=lambda param: param[0])
def simple_db_table_columns(request):
    '''
    Simple database expected columns fixture
    '''
    return request.param
