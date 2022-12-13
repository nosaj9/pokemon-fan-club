from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    Blueprint,
    session,
    g,
)
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import io
import base64

# local
from flask_bcrypt import Bcrypt
from flask import Flask, render_template

import os
# from .users.routes import users
# from .pokemon.routes import pokemon
db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(16)
app.config["MONGODB_HOST"] = "mongodb://localhost:27017/pokemon_rater"
# main = Blueprint("main", __name__)
# app.register_blueprint(main)
from users.routes import users
app.register_blueprint(users)

db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)
login_manager.login_view = "users.login"

from model import PokeClient
poke_client = PokeClient()


from models import User, load_user
from forms import (
    PokemonCommentForm,
    RegistrationForm,
    LoginForm,
    UpdateUsernameForm,
)

from model import PokeClient

@app.route('/')
def index():
    """
    Must show all of the pokemon names as clickable links

    Check the README for more detail.
    """
    
    return render_template('index.html', pokemon_list=poke_client.get_pokemon_list())

@app.route('/pokemon/<pokemon_name>')
def pokemon_info(pokemon_name):
    """
    Must show all the info for a pokemon identified by name

    Check the README for more detail
    """

    return render_template('pokemon.html', pokemon=poke_client.get_pokemon_info(pokemon_name))

@app.route('/ability/<ability_name>')
def pokemon_with_ability(ability_name):
    """
    Must show a list of pokemon 

    Check the README for more detail
    """
    
    return render_template('ability.html', ability=ability_name, ability_pokemon=poke_client.get_pokemon_with_ability(ability_name))
