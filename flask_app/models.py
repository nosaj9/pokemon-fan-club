from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
# from . import config
# from .utils import current_time
import base64


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    favorite_pokemon = db.StringField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class Pokemon(db.Document):
    name = db.StringField(required=True, unique=True)
    likers = db.ListField(db.StringField(required=True, unique=True), default=[])

class Comment(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    pokemon_name = db.StringField(required=True, min_length=1, max_length=40)
