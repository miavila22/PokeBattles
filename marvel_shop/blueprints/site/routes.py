import random
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
# from flask_jwt_extended import c get_jwt_identity, jwt_required
from marvel_shop.forms import AddPokemonForm, BattleForm
from marvel_shop.helpers import get_pokemon_details, color_types
from marvel_shop.models import Pokemon, User, db
from marvel_shop.battle import initialize_trainers, battle_over, reset_pokemon_hp, switch_pokemon
from flask_login import current_user


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def homepage():
    return render_template('homepage.html')

# now I need to have the user be able to add/remove/view their team


@site.route('/add_pokemon/', methods=['GET', 'POST'])
def add_pokemon():


    form = AddPokemonForm()
    
    if form.validate_on_submit():
        current_pokemon_count = Pokemon.query.filter_by(user=current_user).count()

        if current_pokemon_count < 4:
            pokemon_name = form.pokemon_name.data

            new_pokemon = Pokemon(name=pokemon_name, user=current_user)
            db.session.add(new_pokemon)
            db.session.commit()

            flash(f"Successfully added {pokemon_name} to your Pokemon team!", category='success')
            return redirect('/teams')
        else:
            flash("You can only add 4 Pokemon to your team!", category='danger')
    
    return render_template('team_building.html', form=form)


@site.route('/remove_pokemon/<pokemon_id>', methods=['POST'])
def remove_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)

    if not pokemon:
        flash("Pokemon not here!", category='warning')
    else:
        db.session(pokemon)
        db.session.commit()
        flash(f'Successfully removed {pokemon.name} from your team.', category='success')
    
    return redirect('/user_profile', user_id=session.get('user_id'))


# function for battle. started 12/12, continuing 12/13
# for now do a function to have a test battle with a random computer


# def generate_random_pokemon():
#     random_pokemon_name = str(random.randint(1, 1021))  
#     return get_pokemon_details(random_pokemon_name)


# Using potion, can only heal 10HP to pokemon
# can only use 3 per battle
# just like the game, potion takes first priority to whomever uses it. 
        # if form.potion.data:
        #     if user_action.potion_count < 3:
        #         user_action.HP += 10 
        #         user_action.potion_count += 1
        #         flash (f"{user_action} used Potion! 10HP was added", category='success')

        #     else: 
        #         flash("You've already used all your potions! 3 per battle")

# now with the attack. Since you didn't pass a moves[] into your API,
# just make sure that you give a number and a possibility. Since pokemon miss attacks in the game, give small probability. 
# if hp is <= 0, pokemon faints.
# once, the pokemon faints, it should redirect them to another page to send out another. After message is displayed that your pokemon fainted. 
# have to make another HTML for the switching of Pokemon. redirect to url_for(/pokeswitch)
# if either user does not have anymore pokemon, the battle is over and each user will receive a message. 
# possibility of using a dictionary to keep track how many pokemon each user has with. 
        # elif form.attack.data:
        #     opponent_pokemon.hp -= 10

        #     if opponent_pokemon <= 0:
        #         flash (f"{opponent_pokemon.name} fainted!", category='danger')


# switching out Pokemon:
# if each has >= 0, game is over



# how can we use this^ 
# can we possibly store these 2 in a function instead of a new file then bring in "current_user" as an argument then return trainer1,2
# then in the battle function we can call in the function that those 2 trainers are in along with the "current_user"
#

# @site.route('/battle', methods=['GET', 'POST'])
# def pokemon_battle():
#     form = BattleForm()
#     # user_action = Pokemon.query.get_pokemon_details()
#     opponent_pokemon = [get_pokemon_details(random.randint(1, 1000)) for i in range(4)]
#     user_potion = 3
#     opponent_potion = 3

#     if request.method == "POST" and form.validate_on_submit():
#         user_action = trainer1
#         opponent = trainer2

#         #POTION/HEALING PART
#         if form.potion.data:
#             if user_action['potion_count'] < 3:
#                 user_pokemon = user_action['team'][0]
#                 max_hp = get_pokemon_details(user_pokemon['name']['hp'])

#                 if user_pokemon['hp'] < max_hp:
#                     user_pokemon['hp'] += 10
#                     if user_pokemon['hp'] > max_hp:
#                         user_pokemon['hp'] = max_hp

#                     #counter for potions
#                     user_action['potion_count'] += 1
#                     flash(f"{user_pokemon['name']} used Potion! 10HP was restored.", category='success')
#                 else:
#                     flash(f"Your Pokemon is already at full health.", category='info')
#                 #comeback to work on the logic here.
#             else: 
#                 flash("You've already used up all 3 potions! It's only 3 per battle!")

#         #ATTACKING PART
#         elif form.attack.data:
#             if random.random() > 0.2: #this is the probability
#                 opponent_pokemon = opponent['team'][0]
#                 opponent_pokemon['hp'] -= 20

#                 if opponent_pokemon['hp'] <=0:
#                     flash(f"{opponent_pokemon['name']} fainted!", category='warning')
#                     opponent['alive pokemon'] -= 1
            


# @jwt_required()
@site.route("/battle", methods=['GET', 'POST'])
def battle():
    
    trainer1, trainer2 = initialize_trainers(user_id=current_user.user_id)
    trainers = [trainer1, trainer2]

    form = BattleForm()

    if request.method == "POST" and form.validate_on_submit():
        user_action = trainers[0]
        opponent = trainers[1]

        if form.potion.data:
            if user_action['potion_count'] < 3:
                user_pokemon = user_action['team'][0]  #this is going to call your first pokemon from your list. 
                max_hp = get_pokemon_details(user_pokemon['name'])['hp']

                if user_pokemon['hp'] < max_hp:
                    user_pokemon['hp'] += 10
                    if user_pokemon['hp'] > max_hp:
                        user_pokemon['hp'] = max_hp

                    user_action['potion_count'] += 1
                    flash(f"{user_pokemon['name']} used Potion! 10HP was added", category='success')
                else:
                    flash("Your Pokemon is already at full health!", category='info')
            else:
                flash("You've already used all your potions! 3 per battle")

        elif form.attack.data:
            user_pokemon = user_action['team'][0] 
            if random.random() > 0.2:  # This is the probability happening. So you have a 20% chance of missing. 
                opponent_pokemon = opponent['team'][0]  
                opponent_pokemon['hp'] -= 20

                if opponent_pokemon['hp'] <= 0:
                    flash(f"{opponent_pokemon['name']} fainted!", category='danger')
                    opponent['alive_pokemon'] -= 1

                    if battle_over(trainers):
                        flash("Congratulations! You won the battle!", category='success')
                        reset_pokemon_hp(trainers)
                        return redirect(url_for('homepage'))

                    flash(f"Opponent sent out {opponent['team'][0]['name']}!", category='info')

        elif form.switch.data:
            flash(f"You switched to {user_action['team'][0]['name']}!", category='info')

    return render_template("battle.html", trainer1=trainer1, trainer2=trainer2, form=form)
                

