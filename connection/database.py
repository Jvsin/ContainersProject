import flask
from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps

app = flask.Flask("__name__")

collections = {}


def set_mongo_client():
    uri = "mongodb://admin:12345@mongodb"

    mongo = MongoClient(uri, server_api=ServerApi("1"))

    collections["users"] = mongo.containersDatabase.users
    collections["bets"] = mongo.containersDatabase.bets


def find_user(username, password):
    query = {"username": username, "password": password}
    document = collections["users"].find_one(query)

    return document


@app.route("/register", methods=["POST"])
def register():
    try:
        data = flask.request.get_json(force=True)

        username = data["username"]
        password = data["password"]

    except:
        return "Error", 400

    user = find_user(username, password)

    if user:
        return "Error", 400

    collections["users"].insert_one(
        {
            "username": username,
            "password": password,
        }
    )

    return "Ok", 200


@app.route("/login", methods=["POST"])
def login():
    try:
        data = flask.request.get_json(force=True)

        username = data["username"]
        password = data["password"]

    except:
        return "Error", 401

    user = find_user(username, password)

    if not user:
        return "Error", 402

    if user["password"] != password:
        return "Error", 403

    return "Ok", 200


################################################


# @app.route('/submit_scores', methods=['POST'])
def submit_scores():
    # username = request.form['username']
    match_index = request.form["match_index"]
    home_team = request.form["home_team"]
    away_team = request.form["away_team"]
    home_goals = int(request.form["home_goals"])
    away_goals = int(request.form["away_goals"])

    bet = {
        "username": "user1",
        "match_index": int(match_index),
        "home_team": home_team,
        "away_team": away_team,
        "home_goals": home_goals,
        "away_goals": away_goals,
    }

    collections["bets"].update_one(
        {"username": "user1", "match_index": match_index}, {"$set": bet}, upsert=True
    )

    collections["bets"].insert_one(bet)

    return "OK", 200


@app.route("/push-to-mongo", methods=["POST"])
def push_to_mongo():
    try:
        data = flask.request.get_json(force=True)

        collections["bets"].update_one(
            {"match_index": data["match_index"]}, {"$set": data}, upsert=True
        )

        return "OK", 200

    except Exception as e:
        return str(e), 400
    
####################################################################3
@app.route("/get-bets", methods=["POST","GET"])
def load_bets():
    documents = collections["bets"].find()
    print(documents)
    json_documents = dumps(documents)
    return json_documents
 

if __name__ == "__main__":
    set_mongo_client()

    app.run(port=4001, host="0.0.0.0")
