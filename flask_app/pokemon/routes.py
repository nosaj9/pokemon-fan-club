from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from app import bcrypt
from forms import RegistrationForm, LoginForm, UpdateUsernameForm, PokemonCommentForm, FavoritePokemonForm, LikePokemonForm, UnlikePokemonForm
from models import User, Comment, Pokemon
from model import PokeClient
from datetime import datetime
from emoji import emojize
from mongoengine.queryset.visitor import Q

poke_client = PokeClient()

pokemon = Blueprint('pokemon', __name__)

@pokemon.route('/')
def index():
    return render_template('index.html', pokemon_list=poke_client.get_pokemon_list())

@pokemon.route('/pokemon/<pokemon_name>', methods=["GET", "POST"])
def pokemon_info(pokemon_name):
    favorite = FavoritePokemonForm()
    form = PokemonCommentForm()
    like = LikePokemonForm()
    is_like = False

    if current_user.is_authenticated:
        # if a like for this pokemon by this user already exists
        if Pokemon.objects(Q(name=pokemon_name) & Q(likers__contains=current_user.username)):
            like = UnlikePokemonForm()
        else:
            is_like = True

    if form.submit.data and form.validate_on_submit() and current_user.is_authenticated:
        review = Comment(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=datetime.now().strftime("%B %d, %Y at %H:%M:%S"),
            pokemon_name=pokemon_name,
        )
        review.save()

        flash("Comment successfully added!")
        return redirect(request.path)
    elif favorite.submitFavorite.data and favorite.validate_on_submit() and current_user.is_authenticated:
        current_user.modify(favorite_pokemon=pokemon_name)
        current_user.save()

        flash("Favorite Pokemon successfully updated!")
        return redirect(request.path)
    elif like.submitLike.data and like.validate_on_submit() and current_user.is_authenticated:
        if is_like:
            if Pokemon.objects(name=pokemon_name).first() is None:
                pokemon = Pokemon(name = pokemon_name)
                pokemon.save()
            
            pokemon = Pokemon.objects(name=pokemon_name).get()
            pokemon.likers.append(current_user.username)
            pokemon.save()

            flash("Like successfully added!")
            return redirect(request.path)
        else:
            pokemon = Pokemon.objects(name=pokemon_name).update(pull__likers=current_user.username)

            flash("Like successfully removed!")
            return redirect(request.path)

    comments = Comment.objects(pokemon_name=pokemon_name)
    
    num_likes = 0

    if Pokemon.objects(name=pokemon_name).first() is not None:
        num_likes = len(Pokemon.objects.get(name=pokemon_name).likers)

    num_favorited = len(User.objects(favorite_pokemon=pokemon_name))

    return render_template('pokemon.html', 
        pokemon=poke_client.get_pokemon_info(pokemon_name), 
        form=form, 
        num_likes=num_likes,
        comments=comments, 
        like_form=like,
        favorite_form=favorite, 
        num_favorited=num_favorited, 
        info_emoji=emojize(":pencil:"),
        ability_emoji=emojize(":magic_wand:"),
        stats_emoji=emojize(":file_folder:"),
        locations_emoji=emojize(":world_map:"),
        moves_emoji=emojize(":crossed_swords:"),
    )

@pokemon.route('/ability/<ability_name>')
def pokemon_with_ability(ability_name):
    return render_template('ability.html', ability=ability_name, description=poke_client.get_ability_description(ability_name), ability_pokemon=poke_client.get_pokemon_with_ability(ability_name))

@pokemon.route('/about')
def display_about():
    return render_template('about.html')