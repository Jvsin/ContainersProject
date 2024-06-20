import http.client
import json


def getStandings():
    conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "9e5e2785cbmshd7e0f7a68c44835p1fd16fjsndac8dbc9c39d",
        'X-RapidAPI-Host': "api-football-v1.p.rapidapi.com"
    }

    conn.request("GET", "/v3/standings?season=2023&league=39", headers=headers)

    res = conn.getresponse()
    return res.read()

def getResults():
    conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "9e5e2785cbmshd7e0f7a68c44835p1fd16fjsndac8dbc9c39d",
        'X-RapidAPI-Host': "api-football-v1.p.rapidapi.com"
    }

    conn.request("GET", "/v3/fixtures?league=39&season=2023&from=2024-05-10&to=2024-05-14", headers=headers)

    res = conn.getresponse()
    return res.read()

def getMatches():
    data = getResults()
    data = json.loads(data)

    counter = 0
    for match in data['response']:
        print(counter)
        date = match['fixture']['date']
        venue_name = match['fixture']['venue']['name']
        venue_city = match['fixture']['venue']['city']
        status = match['fixture']['status']['long']
        teams_home = match['teams']['home']['name']
        teams_away = match['teams']['away']['name']
        home_goals = match['goals']['home']
        away_goals = match['goals']['away']

        print(f"Data: {date}")
        print(f"{status}")
        print(f"Stadion: {venue_name}, {venue_city}")
        print(f"{teams_home} - {teams_away}")
        if (home_goals != None and away_goals != None):
            print(f"{home_goals}:{away_goals}")
        print()
        counter += 1

def getTableStandings():
    data = getStandings()
    data = json.loads(data)
    for group in data['response'][0]['league']['standings']:
        for place in group:
            rank = place['rank']
            team = place['team']['name']
            points = place['points']
            goalDifference = place['goalsDiff']
            print(f"{rank}. {team} {goalDifference} PTS: {points}")
        print()

getMatches()
getTableStandings()