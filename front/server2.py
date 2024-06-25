import datetime
import uuid

import flask
import flask_session
import requests
from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask("__name__", template_folder="home/front/templates")

connection_uri = "http://connection:4001"
api_uri = "http://api:4002"


def get_mongo_client():
    uri = "mongodb://admin:12345@mongodb"
    mongo = MongoClient(uri, server_api=ServerApi("1"))
    return mongo


def init_sessions(mongo):
    app.config["SESSION_TYPE"] = "mongodb"
    app.config["SESSION_MONGODB"] = mongo
    app.config["SESSION_MONGODB_DB"] = "containersDatabase"
    app.config["SESSION_MONGODB_COLLECT"] = "sessions"
    app.permanent_session_lifetime = datetime.timedelta(hours=24)

    flask_session.Session(app)


def has_registered():
    username = flask.request.form.get("username", "admin")
    password = flask.request.form.get("password", "password")

    response = requests.post(
        f"{connection_uri}/register",
        json={"username": username, "password": password},
    )
    if response.ok:
        flask.session["is_logged_in"] = True
        flask.session["username"] = username
        return True

    return False


def has_logged_in():
    username = flask.request.form.get("username", "admin")
    password = flask.request.form.get("password", "password")

    response = requests.post(
        f"{connection_uri}/login",
        json={"username": username, "password": password},
    )

    if response.ok:
        flask.session["is_logged_in"] = True
        flask.session["username"] = username
        return True

    return False


@app.route("/main_page")
def go_to_main_page():
    return flask.render_template("main_page.html")


@app.route("/")
def index():
    if flask.session.get("is_logged_in", False):
        return flask.render_template("main_page.html")

    return flask.render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST" and has_logged_in():
        return flask.redirect("/")

    return flask.render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if flask.request.method == "POST" and has_registered():
        return flask.redirect("/")

    return flask.render_template("register.html")


@app.route("/logout")
def logout():
    flask.session["is_logged_in"] = False

    return flask.redirect("/")


@app.route("/premier_league", methods=["GET"])
def show_premier_league():

    try:
        response = requests.get(
            f"{api_uri}/premier_league",
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return jsonify({"error": "Failed to fetch data from API"}), 500
    except ValueError as e:
        print(f"JSON decode failed: {e}")
        return jsonify({"error": "Invalid JSON received from API"}), 500

    return flask.render_template("premier_league.html", standings=data)


@app.route("/euro_matches", methods=["GET"])
def show_euro_matches():

    try:
        response = requests.get(
            f"{api_uri}/euro_matches",
        )
        response.raise_for_status()
        matches = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return jsonify({"error": "Failed to fetch data from API"}), 500
    except ValueError as e:
        print(f"JSON decode failed: {e}")
        return jsonify({"error": "Invalid JSON received from API"}), 500

    return flask.render_template("euro_matches.html", matches=matches)


#####################################################################


@app.route("/bet_matches", methods=["GET"])
def set_bets():
    try:
        response = requests.get(
            f"{api_uri}/euro_matches",
        )
        response.raise_for_status()
        matches = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return jsonify({"error": "Failed to fetch data from API"}), 500
    except ValueError as e:
        print(f"JSON decode failed: {e}")
        return jsonify({"error": "Invalid JSON received from API"}), 500

    return flask.render_template("bet_matches.html", matches=matches)


@app.route("/submit_scores", methods=["POST", "GET"])
def submit_scores():
    username = flask.session.get("username", "")
    match_index = int(flask.request.form.get("match_index", 0))
    home_team = flask.request.form.get("home_team", "")
    away_team = flask.request.form.get("away_team", "")
    home_goals = int(flask.request.form.get("home_goals", 0))
    away_goals = int(flask.request.form.get("away_goals", 0))

    bet = {
        "username": username,
        "match_index": match_index,
        "home_team": home_team,
        "away_team": away_team,
        "home_goals": home_goals,
        "away_goals": away_goals,
    }

    response = requests.post(
        f"{connection_uri}/push-to-mongo",
        json=bet,
    )

    if response.status_code == 400:
        print(response.text)

    return flask.redirect("/bet_matches")

@app.route("/check_bets", methods=["POST", "GET"])
def route_check_bets():
    response = requests.get(
        f"{api_uri}/euro_matches",
    )
    response.raise_for_status()
    matches = response.json()

    print(matches)

    response = requests.get(
        f"{connection_uri}/get-bets"
    )
    response.raise_for_status()
    bets = response.json()

    for bet in bets:
        match = next((m for m in matches if m['index'] == bet['match_index']), None)
        if match:
            bet_result = bet['home_goals'] - bet['away_goals']
            match_result = match['home_goals'] - match['away_goals']

            if bet['home_goals'] == match['home_goals'] and bet['away_goals'] == match['away_goals']:
                bet['result'] = "PRAWIDŁOWO"
            elif bet_result == match_result:
                bet['result'] = "WYNIK"
            else:
                bet['result'] = "NIE PRAWIDŁOWO"
        else:
            bet['result'] = "Brak danych o meczu"

    return flask.render_template("check_bets.html", matches=matches, bets=bets)


if __name__ == "__main__":
    mongo = get_mongo_client()
    init_sessions(mongo)

    app.run(port=4000, host="0.0.0.0")
