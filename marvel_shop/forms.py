from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[ DataRequired(), Email()])
    password = PasswordField('Password', validators=[ DataRequired() ])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username', validators= [ DataRequired() ])
    email = StringField('Email', validators= [ DataRequired(), Email() ])
    password = PasswordField('Password', validators= [ DataRequired() ])
    confirm_password = PasswordField('Confirm Password', validators= [ DataRequired(), EqualTo('password') ])
    submit = SubmitField('Sign Up')

#User needs to be able to add and remove pokemon but doesn't need to specify for removal of pokemon
class AddPokemonForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name', validators=[ DataRequired() ])
    search = SubmitField('Search Pokemon')
    submit = SubmitField('Add Pokemon')

class RemovePokemonForm(FlaskForm):
    pokemon_name = StringField("Pokemon Name", validators=[ DataRequired() ])
    submit = SubmitField('Remove Pokemon')

# class SearchPokemonForm(FlaskForm):
#     search = SubmitField('Search Pokemon')

#Battle:
# thoughts no the battle function and possible form for battling if needed.
# how its suppose to look:
# 2 pokemon displayed BUT NOT USING THE Pokemon card design we will only use the sprites. The back_default sprite will appear for the user but the opponents pokemon will show front_default. Kind of like the game.

# the battle portion will give the user 3 different options. Attack, Heal(only 3/whole battle) and switch pokemon. Possible run option but will be counted as a loss.

# The damage dealt for each pokemon will range anywhere from 10-20 (so the battle doesn't last too long.) Get this to work than try to take weaknesses into consideration 
# possibly double damage. or 1.5 damage. 

# when pokemon is sent out flash ('You sent out {pokemon.name}') ('enemy sent out {pokemon.name}')

# Take into consideration of Pokemon's health: can't go below 0, Healing Potion can't heal over their standing HP.

# reset health once battle is over. 

# if user switches pokemon, it should take them to another page to pick another pokemon they have. 

# counter for wins/losses

#Profile: 

#should display wins/losses, pokemon and user name.
# 
class BattleForm(FlaskForm):
    attack = SubmitField('Attack')
    potion = SubmitField('Use Potion')
    switch = SubmitField('Switch')