import http.client
import json




def getResults():
    conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "9e5e2785cbmshd7e0f7a68c44835p1fd16fjsndac8dbc9c39d",
        'X-RapidAPI-Host': "api-football-v1.p.rapidapi.com"
    }

    conn.request("GET", "/v3/fixtures?league=4&season=2024&from=2024-06-14&to=2024-07-26", headers=headers)
    res = conn.getresponse()
    return res.read()

def getStandings():
    conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "9e5e2785cbmshd7e0f7a68c44835p1fd16fjsndac8dbc9c39d",
        'X-RapidAPI-Host': "api-football-v1.p.rapidapi.com"
    }

    conn.request("GET", "/v3/standings?season=2024&league=4", headers=headers)

    res = conn.getresponse()
    return res.read()

def getEuroMatches():
    data = getResults()
    data = json.loads(data)
    for match in data['response']:
        date = match['fixture']['date']
        round = match['league']['round']
        venue_name = match['fixture']['venue']['name']
        venue_city = match['fixture']['venue']['city']
        status = match['fixture']['status']['long']
        teams_home = match['teams']['home']['name']
        teams_away = match['teams']['away']['name']
        home_goals = match['goals']['home']
        away_goals = match['goals']['away']
        
        print(f"Data: {date}, {round}")
        print(f"{status}")
        print(f"Stadion: {venue_name}, {venue_city}")
        if (home_goals != None and away_goals != None):
            print(f"{teams_home} {home_goals}:{away_goals} {teams_away}")
        else: 
            print(f"{teams_home} - {teams_away}")
        print()

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


getEuroMatches()
getTableStandings()