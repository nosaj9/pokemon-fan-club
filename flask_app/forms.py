from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

import re
from models import User
from emoji import emojize

class PokemonCommentForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment " + emojize(":speech_balloon:"))

def password_check(form, field):
    if re.search('[A-Z]', field.data) is None:
        raise ValidationError("Password must have at least one uppercase letter")
    elif re.search('[0-9]', field.data) is None:
        raise ValidationError('Password must contain a number')
    elif re.search('[~!@#\$%^&()?<>,.;:]', field.data) is None:
        raise ValidationError('Password must contain a special symbol')

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=12), password_check])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class LikePokemonForm(FlaskForm):
    submitLike = SubmitField("Like This Pokemon " + emojize(":thumbs_up:"))

class UnlikePokemonForm(FlaskForm):
    submitLike = SubmitField("Unlike This Pokemon " + emojize(":thumbs_down:"))

class FavoritePokemonForm(FlaskForm):
    submitFavorite = SubmitField("Favorite This Pokemon! " + emojize(":green_heart:"))

class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")
