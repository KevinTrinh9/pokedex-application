"""Seed file to make tables for pokedex."""

from models import Pokemon, Type, Generation, Habitat, Ability, Move, db
from app import app

# Create all tables
db.drop_all()
db.create_all()