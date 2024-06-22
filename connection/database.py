import flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = flask.Flask("__name__")

collections = {}

def set_mongo_client():
    uri = "mongodb://admin:12345@mongodb"

    mongo = MongoClient(uri, server_api=ServerApi("1"))

    collections["users"] = mongo.containersDatabase.users

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

if __name__ == "__main__":
    set_mongo_client()

    app.run(port=4001, host="0.0.0.0")