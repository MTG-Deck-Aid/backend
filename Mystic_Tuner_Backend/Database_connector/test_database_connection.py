from database_connector import DatabaseConnector
import pytest

def test_establish_connection():
    instance = DatabaseConnector("localhost", "Mystic_Tuner_Application", "MT_Admin", "admin", 5433)
    assert instance != None

