from Database_Connector.database_connector import DatabaseConnector
import pytest

def test_establish_connection():
    instance = DatabaseConnector("localhost", "Mystic_Tuner_Application", "MT_Admin", "admin", 5433)
    assert instance != None

def test_singleton_instance():
    instance1 = DatabaseConnector.get_instance()
    instance2 = DatabaseConnector.get_instance()

    assert instance1 == instance2

def test_change_connection():
    instance = DatabaseConnector.get_instance()
    result = instance.change_connection()

    assert result == True