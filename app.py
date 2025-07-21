from flask import Flask, jsonify, render_template, request
from nba_api.stats.static import players

app = Flask(__name__)

# Preload all NBA player names (active + historic)
all_players = players.get_players()
player_names = [player['full_name'] for player in all_players]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search_players')
def search_players():
    query = request.args.get('q', '').lower()
    matches = [name for name in player_names if query in name.lower()]
    return jsonify(matches)

if __name__ == '__main__':
    app.run(debug=True)
