from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User, Comment

import requests

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("pokemon.index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful")
    return redirect(url_for("pokemon.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    username_form = UpdateUsernameForm()

    if username_form.validate_on_submit():
        current_user.modify(username=username_form.username.data)
        current_user.save()
        return redirect(url_for("users.account"))
    
    if current_user.favorite_pokemon is not None:
        sess = requests.Session()
        sess.headers.update({'User Agent': 'CMSC388J Spring 2021 Project 2'})
        base_url = 'https://pokeapi.co/api/v2'
        req = f'pokemon/{ current_user.favorite_pokemon }'
        resp = sess.get(f'{base_url}/{req}')

        code = resp.status_code
        if code != 200:
            raise ValueError(f'Request failed with status code: {code} and message: '
                                f'{resp.text}')
            
        resp = resp.json()
            
        result = {}
        result['sprite'] = resp['sprites']

        return render_template(
            "account.html",
            title="Account",
            username_form=username_form,
            pokemon=result
        )
    else:
        result = {}
        result['sprite'] = "None"
        return render_template(
            "account.html",
            title="Account",
            username_form=username_form,
            pokemon=result
        )

@users.route("/user/<username>", methods=["GET", "POST"])
def user_detail(username):
    user = User.objects(username=username).first()
    comments = Comment.objects(commenter=user)

    if user.favorite_pokemon is not None:
        sess = requests.Session()
        sess.headers.update({'User Agent': 'CMSC388J Spring 2021 Project 2'})
        base_url = 'https://pokeapi.co/api/v2'
        req = f'pokemon/{ user.favorite_pokemon }'
        resp = sess.get(f'{base_url}/{req}')

        code = resp.status_code
        if code != 200:
            raise ValueError(f'Request failed with status code: {code} and message: '
                                f'{resp.text}')
            
        resp = resp.json()
            
        result = {}
        result['sprite'] = resp['sprites']

        return render_template("user_detail.html", username=username, favorite_pokemon=user.favorite_pokemon, comments=comments, pokemon=result)
    else:
        result = {}
        result['sprite'] = "None"

        return render_template("user_detail.html", username=username, favorite_pokemon=user.favorite_pokemon, comments=comments, pokemon=result)