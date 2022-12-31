from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from datetime import datetime
import os

from flask_bcrypt import Bcrypt
from flask import Flask, render_template, Blueprint
from flask_talisman import Talisman

db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()

from .users.routes import users
from .pokemon.routes import pokemon

def page_not_found(e):
    return render_template("404.html"), 404

def create_app(test_config=None):
    csp = {
        'script-src': ['https://code.jquery.com/', 'https://cdn.jsdelivr.net/', 'https://stackpath.bootstrapcdn.com/']
    }

    app = Flask(__name__)
    Talisman(app, content_security_policy=csp)
    app.config["SECRET_KEY"] = os.urandom(16)
    #app.config["MONGODB_HOST"] = "mongodb://localhost:27017/pokemon_rater"
    app.config["MONGODB_URI"] = "mongodb+srv://nosaj9:AeibKrBRHj8BzLFD@cluster0.znsncma.mongodb.net/?retryWrites=true&w=majority"
    main = Blueprint("main", __name__)
    app.register_blueprint(main)

    app.register_blueprint(users)
    app.register_blueprint(pokemon)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = "users.login"

    app.register_error_handler(404, page_not_found)

    return app
