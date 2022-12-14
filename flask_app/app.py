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
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# stdlib
from datetime import datetime
import io
import base64

# local
from flask_bcrypt import Bcrypt
from flask import Flask, render_template
from flask_talisman import Talisman

def page_not_found(e):
    return render_template("404.html"), 404

import os

db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()

# pass this into Talisman when ready
csp = {
    'default-src': '\'self\'',
    # 'img-src': '*',
    # 'script-src': '*min.js'
}

app = Flask(__name__)
#Talisman(app, content_security_policy=None)
app.config["SECRET_KEY"] = os.urandom(16)
app.config["MONGODB_HOST"] = "mongodb://localhost:27017/pokemon_rater"
# main = Blueprint("main", __name__)
# app.register_blueprint(main)
from users.routes import users
from pokemon.routes import pokemon
app.register_blueprint(users)
app.register_blueprint(pokemon)

db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)
login_manager.login_view = "users.login"

app.register_error_handler(404, page_not_found)

from model import PokeClient
poke_client = PokeClient()
