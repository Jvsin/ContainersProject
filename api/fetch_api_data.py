import http.client
import json
from datetime import datetime
import time
from flask import Flask, jsonify

app = Flask("__main__")

conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "9e5e2785cbmshd7e0f7a68c44835p1fd16fjsndac8dbc9c39d",
    'X-RapidAPI-Host': "api-football-v1.p.rapidapi.com"
}


def get_results_pl():
    conn.request("GET", "/v3/fixtures?league=39&season=2024&from=2024-08-01&to=2024-08-19", headers=headers)
    
    res = conn.getresponse()
    data = json.loads(res.read())
    
    print(json.dumps(data, indent=4))
    
    return res.read()

def get_standings_pl():

    conn.request("GET", "/v3/standings?season=2024&league=39", headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read())
    
    # print(json.dumps(data, indent=0))
    results = []
    for group in data['response'][0]['league']['standings']:
        for place in group:
            rank = place['rank']
            team = place['team']['name']
            points = place['points']
            goal_diff = place['goalsDiff']
            results.append({
            'rank': rank,
            'team': team,
            'points': points,
            'goalDifference': goal_diff
        })
    print(results)
    return results

@app.route('/premier_league', methods=["GET"])
def get_standings():
    data = get_standings_pl()
    print(data)
    return jsonify(data)


def format_date(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
    
    formatted_date = date_object.strftime('%d %m %Y %H:%M')
    
    return formatted_date

def get_euro_matches():
    conn.request("GET", "/v3/fixtures?league=4&season=2024&from=2024-06-14&to=2024-07-26", headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read())

    result = []
    counter = 0
    for match in data['response']:
        index = counter
        date = match['fixture']['date']
        round = match['league']['round']
        venue_name = match['fixture']['venue']['name']
        venue_city = match['fixture']['venue']['city']
        status = match['fixture']['status']['long']
        teams_home = match['teams']['home']['name']
        teams_away = match['teams']['away']['name']
        home_goals = match['goals']['home']
        away_goals = match['goals']['away']
        if (home_goals == None and away_goals == None):
            home_goals = 0
            away_goals = 0
        result.append({
            'index': index,
            'date': format_date(date),
            'round': round,
            'venue_name': venue_name,
            'venue_city': venue_city,
            'status': status,
            'teams_home': teams_home,
            'teams_away': teams_away,
            'home_goals': home_goals,
            'away_goals': away_goals
        })
        counter += 1
    # print(result)
    return result

@app.route('/euro_matches', methods=["GET"])
def euro_matches():
    data = get_euro_matches()
    print(data)
    return jsonify(data)

###############################################################3

# @app.route('/bet_matches', methods=["GET"])

if __name__ == "__main__":
    app.run(port=4002, host="0.0.0.0")


