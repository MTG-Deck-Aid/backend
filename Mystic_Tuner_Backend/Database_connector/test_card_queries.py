from database_queries import card_queries
from database_connector import DatabaseConnector
import pytest

instance

@pytest.fixture
def setup_and_teardown():
    global instance
    instance = DatabaseConnector("localhost", "Test_Database", "MT_Admin", "admin", 5433)

    yield



def test_create():
    global instance
    

def test_read():
    pass

def test_delete():
    pass




