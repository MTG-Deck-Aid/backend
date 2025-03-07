from Database_Connector.database_connector import database_connector
import pytest

def test_establish_connection():
    instance = database_connector("localhost", "Mystic_Tuner_Application", "MT_Admin", "admin", 5433)
    assert instance != None

def test_singleton_instance():
    instance1 = database_connector.get_instance()
    instance2 = database_connector.get_instance()

    assert instance1 == instance2

def test_change_connection():
    instance = database_connector.get_instance()
    result = instance.change_connection()

    assert result == True