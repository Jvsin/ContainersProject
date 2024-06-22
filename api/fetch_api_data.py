import http.client
import json

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
    # json_result = json.dumps(result, indent=4)
        
    # print(json_result)
    print(results)
    return results

@app.route('/premier_league', methods=["GET"])
def get_standings():
    data = get_standings_pl()
    print(data)
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=4002, host="0.0.0.0")

# get_results_pl()
# get_standings_pl()

