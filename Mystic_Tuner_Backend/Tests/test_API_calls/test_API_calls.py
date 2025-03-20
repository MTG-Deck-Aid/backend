import pytest
import requests
from rest_framework.response import Response
import json
from django.test import Client

from Mystic_Tuner_Backend.scryfall_engine.scryfall_engine import ScryFallEngine

@pytest.fixture
def setup_and_teardown():
    backend_URL = "http://localhost:5000/api/"
    return backend_URL

def test_verify_cards_valid(setup_and_teardown):
    backend_URL = setup_and_teardown
    data = {
        "names": ["Abrade", "Arcane Signet"]
    }
    response = requests.post(backend_URL + "decks/verify-cards/", json=data)
    assert response.status_code == 200
def test_verify_cards_invalid(setup_and_teardown):
    backend_URL = setup_and_teardown
    data = {
        "names": ["Abrade", "Arcane Signet", "Invalid Card"]
    }
    response = requests.post(backend_URL + "decks/verify-cards/", json=data)
    assert response.status_code == 422
def test_get_image_linksValid(setup_and_teardown):
    backend_URL = setup_and_teardown
    data = {
        "name": "Abrade"
    }
    response = requests.get(backend_URL + "decks/get-image-links", json=data)
    assert response.status_code == 200

def test_get_commander(setup_and_teardown):
    backend_URL = setup_and_teardown
    data = {
        "commander": "Krenko, Mob Boss"
    }
    response = requests.post(backend_URL + "decks/commander", json=data)
    assert response.status_code == 200

def test_get_user_decks(setup_and_teardown):
    backend_URL = setup_and_teardown
    data = {
        "user_id": 1
    }
    response = requests.post(backend_URL + "decks/user-decks", json=data)
    assert response.status_code == 200