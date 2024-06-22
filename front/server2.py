import datetime
import uuid

import flask
import flask_session
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = flask.Flask("__name__", template_folder="home/front/templates")

connection_uri = "http://connection:4001"

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
        return True
    return False

@app.route("/main_page")
def go_to_main_page():
    return flask.render_template("main_page.html")

@app.route("/")
def index():
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


if __name__ == "__main__":
    mongo = get_mongo_client()
    init_sessions(mongo)

    app.run(port=4000, host="0.0.0.0")