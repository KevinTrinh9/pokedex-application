from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pokemon, Types, Generations, Habitats, Abilities, Moves
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pokedex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] =  True
app.config['SECRET_KEY'] = "pokemon123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def search_pokemon():
    offset = request.args.get("offset", default=0, type=int)
    limit = 25
    pokemon_list_url = f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}"
    response = requests.get(pokemon_list_url)
    if response.status_code == 200:
        data = response.json()
        pokemon_list = data['results']
        pokemon_sprites = {}
        for pokemon in pokemon_list:
            pokemon_name = pokemon['name'].capitalize()
            pokemon_url = pokemon['url']
            sprite_response = requests.get(pokemon_url)
            if sprite_response.status_code == 200:
                sprite_data = sprite_response.json()
                sprite_url = sprite_data['sprites']['front_default']
                pokemon_sprites[pokemon_name] = sprite_url
        prev_offset = max(0, offset - limit)
        next_offset = offset + limit
        return render_template("search.html", pokemon_list=pokemon_list, pokemon_sprites=pokemon_sprites, prev_offset=prev_offset, next_offset=next_offset)
    else:
        flash("Error retrieving list of Pokemon. Please try again later.")
        return redirect("/")

@app.route("/search")
def search():
    """Obtains search term, and makes request to the PokeAPI to search for specific pokemon"""
    pokemon_name = request.args.get("pokemon_name").lower()
    if not pokemon_name:
        flash("Please enter a Pokemon's name.")
        return redirect("/")
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"
    pokemon_response = requests.get(pokemon_url)
    species_response = requests.get(species_url)

    if pokemon_response.status_code == 200 and species_response.status_code == 200:
        pokemon = pokemon_response.json()
        species = species_response.json()
        sprite = pokemon["sprites"]["front_default"]
        types = ", ".join([type["type"]["name"].capitalize() for type in pokemon["types"]])
        generation = species["generation"]["name"].capitalize().replace("-", " ")
        if generation.startswith("Generation"):
            roman_numeral = generation[10:]
            generation = "Generation " + roman_numeral.upper()
        if "habitat" in species and species["habitat"] is not None:
            habitat = species["habitat"]["name"].capitalize()
        else:
            habitat = "N/A"
        abilities = ", ".join([ability["ability"]["name"].capitalize() for ability in pokemon["abilities"]])
        moves = sorted([move["move"]["name"].capitalize() for move in pokemon["moves"]])
        return render_template("details.html", pokemon=pokemon, species=species, sprite=sprite, types=types, generation=generation, habitat=habitat, abilities=abilities, moves=moves)
    else:
        flash("Pokemon not found. Please try again.")
        return redirect("/")