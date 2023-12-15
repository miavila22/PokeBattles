import decimal
from flask import jsonify
import requests
import requests_cache
import json


# this is where the function needs to pull information back from the PokeAPI 
# reference back to Notion and In_class example 
requests_cache.install_cache()


# I need a way to display the type color according to the pokemon now that I am now calling types from the API
# Maybe do a dictionary to store the types keys, then use a linear gradient to store the values? Double check API to see if it's
# updated or to see if the put a "previous type" or "current type"
# but remember each pokemon can have multiple types like Fire/Flying. Focus on only the Card types. There are 9 types. 
color_types = {
    "normal": 'background: linear-gradient(to bottom, #ffffff, #ededed)',
    "water": 'background: linear-gradient(to bottom, #0bfff0, #00b9ff)',
    "fire": 'background: linear-gradient(to bottom, #f78660, #ff0000)',
    "electric": 'background: linear-gradient(to bottom, #fff582, #c3b400)',
    "fighting": 'background: linear-gradient(to bottom, #ff8900, #aa6600)',
    "psychic": 'background: linear-gradient(to bottom, #b58cfb, #8737ff)',
    "dark": 'background: linear-gradient(to bottom, #454545, #000000)',
    "metal": 'background: linear-gradient(to bottom, #b8b6b6, #626262)',
    "fairy":'background: linear-gradient(to bottom, #feadf9, #f91af7)',
    "grass": 'background: linear-gradient(to bottom, #25f520, #0c8800)',
}
#added 12/9


def get_pokemon_details(pokemon_name):
    #have to get URL but reference back to the pokeAPI(W3)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    response = requests.get(url)

    if response.status_code == 200:
        pokedex = response.json()
        #only return what you need so name, hp, attack , image or sprite for the api
        #now adding types 12/09

        name = pokedex['forms'][0]['name']
        hp = pokedex['stats'][0]['base_stat']
        attack = pokedex['stats'][1]['base_stat']
        defense = pokedex['stats'][2]['base_stat']
        sprite = pokedex['sprites']['front_default']
        types = pokedex['types'][0]['type']['name'] #added 12/09
        sprite2 = pokedex['sprites']['back_default']

        gradient_type = color_types.get(types.lower()) 
        

        poke = {
            "name": name,
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "sprite": sprite,
            "types": types, #added 12/09
            "type_gradient": gradient_type,
            "sprite2": sprite2
        }
        return poke
    
    else: 
        print("That Pokemon does not exist!")


class JSONEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)







