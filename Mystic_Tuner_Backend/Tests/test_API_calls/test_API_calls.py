import pytest
import requests
from rest_framework.response import Response
import json
import time
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
       "Authorization": "Bearer <Token>"
    }
    return backend_URL, header
#TC-AP15
def test_verify_cards_speed(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
      "names": [
        "Abrade",
        "Ambush Viper",
        "Arcane Signet",
        "Bear Umbra",
        "Big Play",
        "Bite Down",
        "Blasphemous Act",
        "Bolt Bend",
        "Branching Evolution",
        "Bulk Up",
        "Bushwhack",
        "Chainsaw",
        "Chandra's Ignition",
        "Choose Your Weapon",
        "Collective Resistance",
        "Cultivate",
        "Cursed Recording",
        "Decimate",
        "Evolution Sage",
        "Exponential Growth",
        "Fangs of Kalonia",
        "Fireshrieker",
        "Forest",
        "Forgotten Ancient",
        "Ghalta, Primal Hunger",
        "Giant Growth",
        "Giant Spectacle",
        "Gift of the Viper",
        "Goblin Anarchomancer",
        "Halana and Alena, Partners",
        "Hardened Scales",
        "Hunter's Insight",
        "Innkeeper's Talent",
        "Llanowar Elves",
        "Luxior, Giada's Gift",
        "Madcap Skills",
        "Mending Touch",
        "Mountain",
        "Mutant's Prey",
        "Naturalize",
        "Ordeal of Nylea",
        "Otherworldly Outburst",
        "Pest Infestation",
        "Pir, Imaginative Rascal",
        "Primal Boost",
        "Pyromancer's Goggles",
        "Quick Draw",
        "Quick-Draw Katana",
        "Ram Through",
        "Reliquary Tower",
        "Return the Favor",
        "Rootbound Crag",
        "Ruby, Daring Tracker",
        "Shock",
        "Smash to Dust",
        "Snakeskin Veil",
        "Sol Ring",
        "Soulstone Sanctuary",
        "Stolen Vitality",
        "Sure Strike",
        "Taurean Mauler",
        "The Ozolith",
        "Thornweald Archer",
        "Titan's Strength",
        "Titanic Growth",
        "Unleash Fury",
        "Unnatural Growth",
        "Utopia Sprawl",
        "Viridian Claw",
        "Wall of Vines",
        "Wilderness Reclamation",
        "Wildwood Scourge",
        "Xenagos, God of Revels"
      ]
    }
    start_time = time.time()
    response = requests.post(backend_URL + "decks/verify-cards/", json=data)
    elapsed_time = time.time() - start_time
    assert elapsed_time < 5
#TC-AP01
def test_verify_cards_valid(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
        "names": ["Abrade", "Arcane Signet"]
    }
    response = requests.post(backend_URL + "decks/verify-cards/", json=data)
    assert response.status_code == 200

#TC-AP02
def test_verify_cards_invalid(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
        "names": ["Abrade", "Arcane Signet", "Invalid Card"]
    }
    response = requests.post(backend_URL + "decks/verify-cards/", json=data)
    assert response.status_code == 422

#TC-AP03
def test_get_image_linksValid(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
        "name": "Abrade"
    }
    response = requests.get(backend_URL + "decks/get-image-links", json=data)
    assert response.status_code == 200

#TC-AP04
def test_get_commander(setup_and_teardown):
    backend_URL, _ = setup_and_teardown
    data = {
        "commander": "Krenko, Mob Boss"
    }
    response = requests.post(backend_URL + "decks/commander", json=data)
    assert response.status_code == 200

#TC-AP05
def test_suggestions(setup_and_teardown):
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

#TC-AP06
def test_suggestions_nochange(setup_and_teardown):
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


#TC-AP07
def test_autocomplete_search(setup_and_teardown):
  backend_URL, _ = setup_and_teardown
  data = {
      "search": "Abr"
  }
  response = requests.get(backend_URL + "decks/autocomplete/", json=data)
  assert response.status_code == 200

#TC-AP08
def test_autocomplete_search_nonsense(setup_and_teardown):
  backend_URL, _ = setup_and_teardown
  data = {
      "search": "!@#$%^&*()_+"
  }
  response = requests.get(backend_URL + "decks/autocomplete/", json=data)
  assert response.status_code == 200


#TC-AP09
def test_get_deck(setup_and_teardown):
  backend_URL, header = setup_and_teardown
  response = requests.get(backend_URL + "decks/deck?deck_id=1", headers=header)
  assert response.status_code == 200

#TC-AP10
def test_get_deck_NonExistent(setup_and_teardown):
  backend_URL, header = setup_and_teardown
  response = requests.get(backend_URL + "decks/deck?deck_id=1000000", headers=header)
  assert response.status_code == 404

#TC-AP11
def test_get_user_decks(setup_and_teardown):
    backend_URL, header = setup_and_teardown
    response = requests.get(backend_URL + "decks/user-decks", headers=header)
    assert response.status_code == 200

#TC-AP12
def test_get_user_decks_notAUser(setup_and_teardown):
    backend_URL, header = setup_and_teardown
    header['Authorization'] = "Bearer definetlyNotanAuthHeader"
    response = requests.get(backend_URL + "decks/user-decks", headers=header)
    assert response.status_code == 401

#TC-AP13
def test_update_deck(setup_and_teardown):
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

#TC-AP14
def test_create_new_deck(setup_and_teardown):
    backend_URL, header = setup_and_teardown
    data = {
    "commander": "Krenko, Mob Boss",
    "deckName": "TESTDECK UNIQUE",
    "deckList": "[{\"name\": \"Mountain\", \"quantity\": 40}]"
    }
    response = requests.post(backend_URL + "new-deck/", json=data, headers=header)
    assert response.status_code == 200


