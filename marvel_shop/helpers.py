import decimal
from flask import jsonify
import requests
import requests_cache
import json


# this is where the function needs to pull information back from the PokeAPI 
# reference back to Notion and In_class example 
requests_cache.install_cache()

def get_pokemon_details(pokemon_name):
    #have to get URL but reference back to the pokeAPI(W3)
    url = "https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"

    response = requests.get(url)

    if response.status_code == 200:
        pokedex = response.json()
        #only return what you need so name, hp, attack , image or sprite for the api

        name = pokedex['forms'][0]['name']
        hp = pokedex['stats'][0]['base_stat']
        attack = pokedex['stats'][1]['base_stat']
        defense = pokedex['stats'][2]['base_stat']
        sprite = pokedex['sprites']['front_default']
        

        poke = {
            "name": name,
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "sprite": sprite
        }
        return jsonify(poke)
    
    else: 
        print("That Pokemon does not exist!")


class JSONEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)







