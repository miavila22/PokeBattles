from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_jwt_extended import current_user
from marvel_shop.forms import AddPokemonForm
from marvel_shop.helpers import get_pokemon_details
from marvel_shop.models import Pokemon, User, db

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def homepage():
    return render_template('homepage.html')

# now I need to have the user be able to add/remove/view their team


@site.route('/add_pokemon/', methods=['GET', 'POST'])
def add_pokemon():


    form = AddPokemonForm()
    
    if form.validate_on_submit():
        pokemon_name = form.pokemon_name.data

        new_pokemon = Pokemon(name=pokemon_name, user=current_user)
        db.session.add(new_pokemon)
        db.session.commit()

        flash(f"Successfully added {pokemon_name} to your Pokemon team!", 'success')
        return redirect('/teams')
    
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
