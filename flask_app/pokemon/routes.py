from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from app import bcrypt
from forms import RegistrationForm, LoginForm, UpdateUsernameForm, PokemonCommentForm, FavoritePokemonForm
from models import User, Comment
from model import PokeClient
from datetime import datetime

poke_client = PokeClient()

pokemon = Blueprint('pokemon', __name__)

@pokemon.route('/')
def index():
    """
    Must show all of the pokemon names as clickable links

    Check the README for more detail.
    """
    
    return render_template('index.html', pokemon_list=poke_client.get_pokemon_list())

@pokemon.route('/pokemon/<pokemon_name>', methods=["GET", "POST"])
def pokemon_info(pokemon_name):
    """
    Must show all the info for a pokemon identified by name

    Check the README for more detail
    """
    favorite = FavoritePokemonForm()
    form = PokemonCommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Comment(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=datetime.now().strftime("%B %d, %Y at %H:%M:%S"),
            pokemon_name=pokemon_name,
        )
        review.save()

        return redirect(request.path)
    elif favorite.validate_on_submit() and current_user.is_authenticated:
        current_user.modify(favorite_pokemon=pokemon_name)
        current_user.save()

        return redirect(request.path)

    comments = Comment.objects(pokemon_name=pokemon_name)
    num_favorited = len(User.objects(favorite_pokemon=pokemon_name))

    return render_template('pokemon.html', pokemon=poke_client.get_pokemon_info(pokemon_name), form=form, comments=comments, favorite_form=favorite, num_favorited=num_favorited)

# currently no way to access on website besides manually typing the url
@pokemon.route('/ability/<ability_name>')
def pokemon_with_ability(ability_name):
    """
    Must show a list of pokemon 

    Check the README for more detail
    """
    
    return render_template('ability.html', ability=ability_name, ability_pokemon=poke_client.get_pokemon_with_ability(ability_name))