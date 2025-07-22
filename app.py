from flask import Flask, render_template, request, jsonify, session
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import random
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

# Team data
#team_abvs = ['ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA',
#             'MIL', 'MIN', 'NYK', 'NOH', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

team_abvs = ['1610612737', '1610612738', '1610612751', '1610612766', '1610612741', '1610612739', '1610612742', '1610612743',
             '1610612765', '1610612744', '1610612745', '1610612754', '1610612746', '1610612747', '1610612763', '1610612748',
             '1610612749', '1610612750', '1610612752', '1610612740', '1610612760', '1610612753', '1610612755', '1610612756',
             '1610612757', '1610612758', '1610612759', '1610612761', '1610612762', '1610612764']

teams_names = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls',
               'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors',
               'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
               'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New York Knicks', 'New Orleans Pelicans',
               'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trailblazers',
               'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']

all_players = players.get_players()
player_names = [p['full_name'] for p in all_players]

def get_player_id(player_name):
    for player in all_players:
        if player_name.lower() == player['full_name'].lower():
            return player['id']
    return None

def get_teams_player_played_for(player_id):
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    time.sleep(1.0)
    df = career.get_data_frames()[0]
    return set(df['TEAM_ID'].dropna().unique())

def get_team_abbreviation(team_name):
    if team_name in teams_names:
        return team_abvs[teams_names.index(team_name)]
    return None

@app.route('/')
def index():
    session['score'] = 0  # Start new session
    team_one = random.choice(teams_names)
    team_two = random.choice(teams_names)
    while team_one == team_two:
        team_two = random.choice(teams_names)
    return render_template('index.html', team_one=team_one, team_two=team_two, player_names=player_names, score=session['score'])

@app.route('/check_player', methods=['POST'])
def check_player():
    player_name = request.form.get('playerName')
    team_one = request.form.get('teamOne')
    team_two = request.form.get('teamTwo')

    team_one_abv = get_team_abbreviation(team_one)
    team_two_abv = get_team_abbreviation(team_two)
    print(team_one_abv, team_two_abv)

    player_id = get_player_id(player_name)
    if not player_id:
        return jsonify({
            "status": "error",
            "message": f"No NBA player found with the name '{player_name}'.",
            "score": session.get('score', 0)
        })

    teams_played_for = str(get_teams_player_played_for(player_id))
    print(teams_played_for)

    if team_one_abv in teams_played_for and team_two_abv in teams_played_for:
        session['score'] = session.get('score', 0) + 1
        return jsonify({
            "status": "success",
            "message": f"✅ Yes, {player_name} has played for both {team_one} and {team_two}.",
            "score": session['score']
        })
    else:
        session['score'] = 0
        return jsonify({
            "status": "fail",
            "message": f"❌ No, {player_name} has not played for both {team_one} and {team_two}.",
            "score": session['score']
        })

@app.route('/next_teams', methods=['GET'])
def next_teams():
    team_one = random.choice(teams_names)
    team_two = random.choice(teams_names)
    while team_one == team_two:
        team_two = random.choice(teams_names)
    return jsonify({
        'team_one': team_one,
        'team_two': team_two,
        'score': session.get('score', 0)
    })

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term', '').lower()
    matches = [name for name in player_names if term in name.lower()]
    return jsonify(matches[:10])

if __name__ == '__main__':
    app.run(debug=True)
