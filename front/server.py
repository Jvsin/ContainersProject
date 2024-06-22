import datetime
import uuid

import flask
import flask_session
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = flask.Flask("__name__", template_folder="home/front/templates")
collections = {}

def get_mongo_client():
    uri = "mongodb://admin:12345@mongodb"

    mongo = MongoClient(uri, server_api=ServerApi("1"))
    collections["users"] = mongo.containersDatabase.users
    
    return mongo

def init_sessions(mongo):
    app.config["SESSION_TYPE"] = "mongodb"
    app.config["SESSION_MONGODB"] = mongo
    app.config["SESSION_MONGODB_DB"] = "containersDatabase"
    app.config["SESSION_MONGODB_COLLECT"] = "sessions"
    app.permanent_session_lifetime = datetime.timedelta(hours=24)

    flask_session.Session(app)

def find_user(username, password):
    query = {"username": username, "password": password}
    document = collections["users"].find_one(query)
    
    return document

def has_logged_in():
    username = flask.request.form.get("username", "admin")
    password = flask.request.form.get("password", "password")

    # response = requests.post(
    #     f"{database_base_url}/login",
    #     json={"username": username, "password": password},
    # )

    # if response.ok:
    #     return True


    if find_user(username, password):
        flask.session["is_logged_in"] = True
        return True

    return False

# def set_mongo_client():
#     uri = f"mongodb://admin:password@mongodb"

#     mongo = MongoClient(uri, server_api=ServerApi("1"))

#     collections["session_data"] = mongo.gierka.session_data
#     collections["auth"] = mongo.gierka.auth

@app.route("/main_page")
def go_to_main_page():
    return flask.render_template("main_page.html")

@app.route("/")
def index():
    # set_session_id()
    # init_mongo()

    # messages = get_messages()
    # init_assistant(messages)

    if flask.session.get("is_logged_in", False):
        return flask.redirect("/main_page")

    return flask.render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST" and has_logged_in():
        flask.session["is_logged_in"] = True

        return flask.redirect("/")

    return flask.render_template("login.html")

def create_new_user(username, password):
    collections["users"].insert_one(
        {
            "username": username,
            "password": password,
            # dodać tutaj nowe pola
        }
    )

def has_registered():
    username = flask.request.form.get("username", "admin")
    password = flask.request.form.get("password", "password")

    # response = requests.post(
    #     f"{database_base_url}/register",
    #     json={"username": username, "password": password},
    # )

    # if response.ok:
    #     return True

    if not find_user(username, password):
        create_new_user(username, password)
        return True
    
    return False

@app.route("/register", methods=["POST", "GET"])
def register():
    if flask.request.method == "POST" and has_registered():
        flask.session["is_logged_in"] = True

        return flask.redirect("/")

    return flask.render_template("register.html")

@app.route("/logout")
def logout():
    flask.session["is_logged_in"] = False

    return flask.redirect("/")


if __name__ == "__main__":
    mongo = get_mongo_client()
    init_sessions(mongo)

    app.run(port=4000, host="0.0.0.0")