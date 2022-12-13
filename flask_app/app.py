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
from forms import (
    PokemonCommentForm,
    RegistrationForm,
    LoginForm,
    UpdateUsernameForm,
)
from models import User, Comment, load_user

from flask import Flask, render_template

from model import PokeClient
# from .users.routes import users
# from .pokemon.routes import pokemon

app = Flask(__name__)
# main = Blueprint("main", __name__)
# app.register_blueprint(main)
# app.register_blueprint(users)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

db = MongoEngine()
bcrypt = Bcrypt()

poke_client = PokeClient()

db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)

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

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        #change to "login" later
        return redirect(url_for("index"))

    return render_template("register.html", title="Register", form=form)