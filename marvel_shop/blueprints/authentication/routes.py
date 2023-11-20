from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, logout_user
from marvel_shop.helpers import get_pokemon_details

#internal imports
from marvel_shop.models import Pokemon, User, db
from marvel_shop.forms import RegisterForm, LoginForm


authentication = Blueprint('authentication', __name__, template_folder='authentication_templates')

@authentication.route('/signup', methods=['GET', 'POST'])
def signup():

    register_form = RegisterForm()

    if request.method == 'POST' and register_form.validate_on_submit():

        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        print(email, password, username)

        if User.query.filter(User.username == username ).first():
            flash(f'Username already exists! Please Try Again', category='warning')
            return redirect('/signup') #learned that I can do return redirect(url_for(then specify the rest))
        
        if User.query.filter(User.email == email).first():
            flash("Email already exist. Please Try Again", category='warning')
            return redirect('/signup')
        
        user = User(username, email, password, first_name, last_name)
        

        db.session.add(user)
        db.session.commit()

        flash(f"You have successfully registered user {username}", category='success')
        return redirect('/signin')
    
    return render_template('sign_up.html', form=register_form)

@authentication.route('/signin', methods=['GET', 'POST'])
def signin():
    
    login_form = LoginForm()

    if request.method == 'POST' and login_form.validate_on_submit():

        email = login_form.email.data
        password = login_form.password.data
        print("login info", email, password)

        user = User.query.filter(User.email == email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Successfully logged in {email}', category='success')
            return redirect('/')
        else:
            flash("Invalid Email or Password, Please Try Again!", category='warning')
            return redirect('/signin')
        
    return render_template('sign_in.html', form=login_form)

@authentication.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@authentication.route('/teams')
def view_team():
    user_team = get_user_team(current_user.user_id)

    if user_team is None:
        return render_template('teams.html', team=[])
    

    return render_template('teams.html', team=user_team)

def get_user_team(user_id):
    user = User.query.get(user_id)
    if user:
        return user.pokemon_team
    return None


# @authentication.route('/profile', methods=['GET','POST'])
# def profile():
#     trainer = current_user
#     register_form = RegisterForm()
#     if request.method == "POST" and register_form.validate_on_submit():
#         username = register_form.username.data
#         email = register_form.email.data
#         password = register_form.password.data
#         first_name = register_form.first_name.data
#         last_name = register_form.last_name.data

#         flash("Profile was Successfully updated!", category='success')
#         return render_template(url_for('profile'))#COME BACK TO THIS!!!!!!!!!!!!!!!!!!!!!!!!
#     else:
#         flash('Invalid input. Try Again!', category='warning')
#         return render_template('profile.html', register_form=register_form)


    
            



@authentication.route('/Pokemon/stats', methods = ['GET', 'POST'])
def get_pokemon_data():

    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        pokemon_name = request.form['pokemon']

        pokemon_details = get_pokemon_details(pokemon_name)

        if pokemon_name:
            new_pokemon = Pokemon(

                name=pokemon_details['name'],
                hp=pokemon_details['hp'],
                attack=pokemon_details['attack'],
                user=user
            )

            db.session.add(new_pokemon)
            db.session.commit()

    return render_template('profile.html', user=user)