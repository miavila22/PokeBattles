from marvel_shop.models import Pokemon
from marvel_shop.helpers import get_pokemon_details
import random
from flask_login import current_user


def initialize_trainers(user_id):
    
    my_pokemon = Pokemon.query.filter_by(user_id=user_id).all()
    trainer1 = {
        'alive_pokemon': len(my_pokemon),
        'team': my_pokemon,
        'potions': 3,
        
    }

    trainer2 = {
        'alive_pokemon': 4,
        'team': [get_pokemon_details(random.randint(1, 1000)) for _ in range(4)],
        'potions': 3,
        
    }

    # for pokemon in trainer2['team']:
    #     pokemon['sprite'] = get_pokemon_details(pokemon['name'])['sprite']

    return trainer1, trainer2 
    
#need to reset the pokemon health after battle so it doesn't stay at 0 
def reset_pokemon_hp(trainers):
    for trainer in trainers:
        for pokemon in trainer['team']:
            pokemon['hp'] = get_pokemon_details(pokemon['name'])['hp']

def battle_over(trainers):
    for trainer in trainers:
        if trainer['alive_pokemon'] == 0:
            return True
    return False

def switch_pokemon(trainer, new_pokemon_index):
   if 0 <= new_pokemon_index < len(trainer['team']):
       trainer['team'][0], trainer['team'][new_pokemon_index] = trainer['team'][new_pokemon_index], trainer['team'][0]
