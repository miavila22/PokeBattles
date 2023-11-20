from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
import uuid
from flask_marshmallow import Marshmallow

from .helpers import get_pokemon_details
from datetime import datetime


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(user_id)




#Create your tables first. 
#Classes: User, Pokemon for now but we can come back if we want to add more. 

class User(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    username = db.Column(db.String(150), nullable=False, unique=True) #needs to be nullable
    email = db.Column(db.String(150), nullable=False, unique=True) #needs to be nullable
    password = db.Column(db.String(200), nullable=False) #needs to be nullable
    #in the Notion, there is an option for a "date_added" for the User but maybe we can skip that. 
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #need to add wins and losses and there has to be a relationship between the user and pokemon table
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    pokemon_team = db.relationship('Pokemon', backref='user', lazy=True)

# METHODS INSERT INTO() 
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id() #have to define set_id 
        self.first_name = first_name
        self.last_name = last_name
        self.username = username 
        self.email = email 
        self.password = self.set_password(password) 

    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"<User: {self.username}>"


# Now youre at the "Creating Our Shop"
# Now create a Page where a user can find other users (so display all users in the database) and then attack that user.
# When you press a button like Attack next to the users name it should bring you to a page that shows your pokemon and their stats and the front_shiny image  
# and the user you are attacking stats and front_shiny image (as an image)
# Determine a method of determining a winner, note you have stats like Hit Points (hp) Base Defense points and base attack points.  
# You can also grab any other information you like from the pokemon.  You could even build out different rules for different abilities.  
# The options here are endless, have some fun with this.
# the instructions give you the attributes for the class. 
    
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    sprite = db.Column(db.String, nullable=False)
    #might have to add the user_id as a Foreign Key but move and BUT COME BACK TO THIS
    user_id = db.Column(db.String, db.ForeignKey(User.user_id), nullable=False)

    def __init__(self, name, hp, attack, defense, user_id, sprite=""):
        
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sprite = self.set_sprite(sprite, name)
        self.user_id = user_id 

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_sprite(self, sprite, name):
        if not sprite:
            pass



