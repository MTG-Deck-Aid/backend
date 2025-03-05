from Database_Connector.database_connector import database_connector
import pytest

def test_establish_connection():
    instance = database_connector("localhost", "Mystic_Tuner_Application", "MT_Admin", "admin", 5433)
    assert instance != None

