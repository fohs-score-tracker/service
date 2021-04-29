"""
Add, edit, and remove players.
"""
from secrets import token_urlsafe
from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError
from ..model import *
from .utils import hash_pw, is_apart_of_team, require_login



router = APIRouter()
router.post('/players/{int:id}/edit')
async def edit_player(id):
    player = Player.query.get(id)
    if not player:
        flask.flash(f"User (ID: <code>{id}</code>) not found.", "danger")
        return flask.redirect(flask.url_for("admin.users"))
    if request.form.get("username"):
            player.username = request.form['username']
        if request.form.get("full_name"):
            player.full_name = request.form['full_name']
        if request.form.get("password"):
            player.pw_hash = hash_pw(request.form['password'], player.pw_salt)

        db.session.add(player)
        try:
            db.session.commit()
        except IntegrityError:
            return 500
        else:
            # TODO redirect to current player
            return 200


@player_manager.route("/players/add", methods=("GET", "POST"))
@require_login
def add_player():
    if request.method == "POST":
        pw_salt = token_urlsafe()
        pw_hash = hash_pw(request.form["password"], pw_salt)
        new_player = Player(
            full_name=request.form["full_name"],
            username=request.form["username"],
            pw_hash=pw_hash,
            pw_salt=pw_salt,
            two_pointers=request.form["two_pointers"],
            missed_two_pointers=0,
            three_pointers=request.form["three_pointers"],
            missed_three_pointers=0,
            user_id=session['user_id'])
        db.session.add(new_player)
        try:
            db.session.commit()
        except IntegrityError:
            flask.flash("User already exists.", "warning")
        else:
            flask.flash('User successfully created.', 'success')
            return flask.redirect(flask.url_for("player_manager.view"))
    return flask.render_template("player/new-player.jinja2")


@player_manager.route("/players/<int:id>/delete")
@require_login
@is_apart_of_team
def delete_player(id):
    player = Player.query.get(id)
    if player:
        db.session.delete(player)
        db.session.commit()
        flask.flash("User successfully removed.", "success")
    else:
        flask.flash("Unknown user", "danger")
        # TODO redirect to somewhere else than here.
    if Player.query.filter_by(
            user_id=flask.session["user_id"]).first() is not None:
        return flask.redirect(flask.url_for("player_manager.view"))
    else:
        flask.flash("You have delete all your players.", category="warning")
        return flask.redirect(flask.url_for("index"))


@player_manager.route("/players/<int:id>/view", methods=("GET", "POST"))
@require_login
@is_apart_of_team
# TODO add Redirect for play to create their first player.
def team_view(id):
    target_player = Player.query.get(id)
    if request.method == "GET":
        players = Player.query.filter_by(user_id=session['user_id']).all()
        return flask.render_template(

            "/player/team_view.jinja2", players=players, player_selected=target_player)

    elif request.method == "POST":
        if(request.form.get("two_pointers")):
            target_player.two_pointers = int(request.form["two_pointers"]) + \
                target_player.two_pointers
        if (request.form.get("three_pointers")):
            target_player.three_pointers = int(
                request.form["three_pointers"]) + target_player.three_pointers
        if request.form.get("missed_three_pointers"):
            target_player.missed_three_pointers = int(
                request.form["missed_three_pointers"])

        db.session.add(target_player)
        try:
            db.session.commit()
        except IntegrityError:
            flask.abort(500)
        return flask.redirect(flask.url_for(
            "player_manager.team_view", id=target_player.id))
    else:
        return flask.abort(405)


@player_manager.route("/players/view")
@require_login
def view():
    target_player = Player.query.filter_by(user_id=session["user_id"]).first()
    if target_player is None:
        return flask.redirect(flask.url_for("player_manager.add_player"))
    else:
        return flask.redirect(flask.url_for(
            "player_manager.team_view", id=target_player.id))
