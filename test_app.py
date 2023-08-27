import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
from app import app, search_pokemon, search

class PokemonTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_search_pokemon(self):
        with app.test_client() as client:
            response = client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Search for a Pokemon", response.data)

    def test_search(self):
        with app.test_client() as client:
            response = client.get("/search?pokemon_name=pikachu")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Pikachu", response.data)

if __name__ == '__main__':
    unittest.main()