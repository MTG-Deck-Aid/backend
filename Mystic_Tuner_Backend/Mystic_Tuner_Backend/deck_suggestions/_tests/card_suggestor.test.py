"""
Unit Testing File for card_suggestor.py
"""

import unittest
from unittest.mock import patch

from backend.Mystic_Tuner_Backend.Mystic_Tuner_Backend.card import Card
from backend.Mystic_Tuner_Backend.Mystic_Tuner_Backend.deck import Deck
from backend.Mystic_Tuner_Backend.Mystic_Tuner_Backend.deck_suggestions.card_suggestor import (
    CardSuggestor,
)
