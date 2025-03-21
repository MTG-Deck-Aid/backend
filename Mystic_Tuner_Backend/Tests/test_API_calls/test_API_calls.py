import pytest
import requests
from rest_framework.response import Response
import json
from django.test import Client

from Mystic_Tuner_Backend.scryfall_engine.scryfall_engine import ScryFallEngine

'''




VERY IMPORTANT FOR THIS TEST FILE TO WORK:
LOOK AT README!!!!!






'''

@pytest.fixture
def setup_and_teardown():
    backend_URL = "http://localhost:5000/api/"
    header = {
       "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjA3TVFNMVZ4bTY5ME14OXBfb2ZvWSJ9.eyJpc3MiOiJodHRwczovL2Rldi00ZmtudG5rb2xyYnNwY3pzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2RiOTc0YjVkNWFkYTkwZmFlNGMwMjIiLCJhdWQiOlsiaHR0cHM6Ly9kZXYtNGZrbnRua29scmJzcGN6cy51cy5hdXRoMC5jb20vYXBpL3YyLyIsImh0dHBzOi8vZGV2LTRma250bmtvbHJic3BjenMudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc0MjQ0NDM3MiwiZXhwIjoxNzQyNTMwNzcyLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXpwIjoiNE50WXVqQlBTYkRTa1V1UUs1MU56WXhvMnBsQUFGVm8ifQ.eAzA6v5ZXDt8QwcWyu___CCm8cT3Mb_EDMXkHTV9PYb3MSd-rh-7fFny3rOfAfkW8gXI5A7ijDipm_bj3fIt9IEZmMHhKp4uXHx3IopcwfFDTL80j-fxyH0DW0jK4YabGGjeAplKioKsMKwkJBFjNqbp3eeOHXdUbi3i33sDjXtXyWc8SA3aKHsuGvVD9i0FTMOknw8VUHsafnlYtetqdq6l-cS_VY3aTseiYOSIeR0I-Y4Xyh6tFc1dQ_EgbzyNafcbRuKQvJGmwJuIm_3rcJcfIoyFIsodga5778eTZCrKnEK7mD_m5e49Fe1Xk2N-0TXJJGmahNN0P9zBiX_iaA"
    }
    return backend_URL, header

def est_verify_cards_valid(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
        "names": ["Abrade", "Arcane Signet"]
    }
    response = requests.post(backend_URL + "decks/verify-cards/", json=data)
    assert response.status_code == 200
def est_verify_cards_invalid(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
        "names": ["Abrade", "Arcane Signet", "Invalid Card"]
    }
    response = requests.post(backend_URL + "decks/verify-cards/", json=data)
    assert response.status_code == 422
def est_get_image_linksValid(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
        "name": "Abrade"
    }
    response = requests.get(backend_URL + "decks/get-image-links", json=data)
    assert response.status_code == 200

def est_get_commander(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
        "commander": "Krenko, Mob Boss"
    }
    response = requests.post(backend_URL + "decks/commander", json=data)
    assert response.status_code == 200

def est_suggestions(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
  "num_to_add": 1,
  "num_to_remove": 2,
  "decklist": {
    "commander": "Marchesha The Black Rose",
    "mainboard": [
      {
        "name": "Ashnod's Al",
        "quantity": 1
      },
      {
        "name": "Demonic Tut",
        "quantity": 1
      },
      {
        "name": "Counterspell",
        "quantity": 1
      },
      {
        "name": "Sol Ring",
        "quantity": 1
      },
      {
        "name": "Swamp",
        "quantity": 9
      },
      {
        "name": "Island",
        "quantity": 9
      },
      {
        "name": "Mountain",
        "quantity": 12
      }
    ]
  }
}

    response = requests.post(backend_URL + "suggestions/", json=data)
    assert response.status_code == 200

def est_suggestions_nochange(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
  "num_to_add": 0,
  "num_to_remove": 0,
  "decklist": {
    "commander": "Marchesha The Black Rose",
    "mainboard": [
      {
        "name": "Ashnod's Al",
        "quantity": 1
      },
      {
        "name": "Demonic Tut",
        "quantity": 1
      },
      {
        "name": "Counterspell",
        "quantity": 1
      },
      {
        "name": "Sol Ring",
        "quantity": 1
      },
      {
        "name": "Swamp",
        "quantity": 9
      },
      {
        "name": "Island",
        "quantity": 9
      },
      {
        "name": "Mountain",
        "quantity": 12
      }
    ]
  }
}

    response = requests.post(backend_URL + "suggestions/", json=data)
    assert response.status_code == 200


def est_autocomplete_search(setup_and_teardown):
  backend_URL, _ = setup_and_teardown
  data = {
      "search": "Abr"
  }
  response = requests.get(backend_URL + "decks/autocomplete/", json=data)
  assert response.status_code == 200


def est_autocomplete_search_nonsense(setup_and_teardown):
  backend_URL = setup_and_teardown
  data = {
      "search": "!@#$%^&*()_+"
  }
  response = requests.get(backend_URL + "decks/autocomplete/", json=data)
  assert response.status_code == 200



def est_get_deck(setup_and_teardown):
  backend_URL, header = setup_and_teardown
  response = requests.get(backend_URL + "decks/deck?deck_id=1", headers=header)
  assert response.status_code == 200

def est_get_deck_NonExistent(setup_and_teardown):
  backend_URL, header = setup_and_teardown
  response = requests.get(backend_URL + "decks/deck?deck_id=1000000", headers=header)
  assert response.status_code == 404

def est_get_user_decks(setup_and_teardown):
    backend_URL, header = setup_and_teardown
    response = requests.get(backend_URL + "decks/user-decks", headers=header)
    assert response.status_code == 200

def est_get_user_decks_notAUser(setup_and_teardown):
    backend_URL, header = setup_and_teardown
    header['Authorization'] = "Bearer definetlyNotanAuthHeader"
    response = requests.get(backend_URL + "decks/user-decks", headers=header)
    assert response.status_code == 401

def est_update_deck(setup_and_teardown):
    backend_URL, header = setup_and_teardown
    data = {
        "deck_id": 1,
        "cardsAdded": [
            {
                "name": "Sol Ring",
                "quantity": 1
            }
        ],
        "cardsRemoved": [
            {
                "name": "Sol Ring",
                "quantity": 1,
            }]
    }
    response = requests.patch(backend_URL + "decks/update/", json=data, headers=header)
    assert response.status_code == 200
def est_create_new_deck(setup_and_teardown):
    backend_URL, header = setup_and_teardown
    data = {
    "commander": "Krenko, Mob Boss",
    "deckName": "justmountain",
    "deckList": "[{\"name\": \"Mountain\", \"quantity\": 40}]"
}
    response = requests.post(backend_URL + "new-deck/", json=data, headers=header)
    assert response.status_code == 200


