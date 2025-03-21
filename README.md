# Mystic Tuner Backend

This the backend for our project, please follow the following links to view the various features of our backend.

## [Database connector](./Mystic_Tuner_Backend/Database_Connector/database_connector.py)

Handles communication between the backend and the PostGreSQL database

## [Deck Suggestor](./Mystic_Tuner_Backend/Mystic_Tuner_Backend/deck_suggestions/deck_suggestion_controller.py)

Handles the LLM functionality of our website.  Sends requests and receives the AI's response.

## [ScryFall Engine](./Mystic_Tuner_Backend/Mystic_Tuner_Backend/scryfall_engine/scryfall_engine.py)

Handles getting/validating card information with the ScryFall API.

## [APIS](./Mystic_Tuner_Backend/restapis/views.py)

Contains all the API route implementation between the frontend and backend.

## [Tests](./Mystic_Tuner_Backend/Tests/__init__.py)

Contains all the pytest testing files.  Please see the different test files.