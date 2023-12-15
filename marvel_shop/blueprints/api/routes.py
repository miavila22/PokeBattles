from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for
from flask_jwt_extended import create_access_token, jwt_required
from flask_login import current_user
from marvel_shop.models import User, Pokemon, db

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/token', methods = ['GET', 'POST'])
def token():
    data = request.json
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id) #just needs a unique identifier
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status': 400,
            'message': 'Missing Client Id. Try Again'
        }
    
# now we need to see the pokemon details and possible add even the user stats for W/L

@api.route('/pokemon/<int:pokemon_id>')
@jwt_required()
def get_pokemon_details(pokemon_id):
   
    pokemon = Pokemon.query.filter_by(id=pokemon_id, user_id=current_user.user_id).first()

    if not pokemon:
        flash('Pokemon not found.', category='warning') 
        return redirect('/homepage')

    pokemon_details = {
        'name': pokemon.name,
        'hp': pokemon.hp,
        'attack': pokemon.attack,
        'defense': pokemon.defense,
        'sprite': pokemon.sprite,
        'types': pokemon.types, #added 12/09
        'type_gradient': pokemon.gradient_type
    }

    return jsonify(pokemon_details)

@api.route('/user_stats')
@jwt_required()
def get_user_stats():
    # Wins/Loses or can I just implement this if I do a user profile? 
    user_stats = {
        'username': current_user.username,
        'wins': current_user.wins,
        'losses': current_user.losses,
    }

    return jsonify(user_stats)