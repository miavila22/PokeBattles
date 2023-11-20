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
    submit = SubmitField('Add Pokemon')

class RemovePokemonForm(FlaskForm):
    pokemon_name = StringField("Pokemon Name", validators=[ DataRequired() ])
    submit = SubmitField('Remove Pokemon')