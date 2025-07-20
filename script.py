from nba_api.stats.static import players, teams
import time
from nba_api.stats.endpoints import playercareerstats
import random

team_abvs = ['ATL', 'BOS', 'NJN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA',
        'MIL', 'MIN', 'NYK', 'NOH', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

teams_names = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls',
                'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors',
                'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
                'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New York Knicks', 'New Orleans Pelicans',
                'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trailblazers',
                'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']

def get_player_id(player_name):
    all_players = players.get_players()
    for player in all_players:
        if player_name.lower() == player['full_name'].lower():
            return player['id']
    return None

def get_team_names():
    return [team['full_name'] for team in teams.get_teams()]

def get_teams_player_played_for(player_id):
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    time.sleep(1)  # avoid rate limiting

    df = career.get_data_frames()[0]  # This is a DataFrame with player’s seasons

    teams_played_for = set(df['TEAM_ABBREVIATION'].dropna().unique())
    return teams_played_for

def get_team_abbreviation(team_name):
    # Gets teams abbreviation
    index = 0
    for name in teams_names:
        if team_name == name:
            team_abv = team_abvs[index]
        index += 1

    return team_abv

def main():
    # Main game loop
    continue_game = True
    score = 0
    while continue_game:
        # Randomly get two teams
        team_name_one = random.choice(teams_names)
        team_name_two = random.choice(teams_names)

        # Ensure that the teams aren't the same
        while team_name_one == team_name_two:
            random.choice(teams_names)

        print("Team One:", team_name_one)
        print("Team Two:", team_name_two)

        team_one_abv = get_team_abbreviation(team_name_one)
        team_two_abv = get_team_abbreviation(team_name_two)
        
        player_name = input("Enter the NBA player's full name: ").strip()
        player_id = get_player_id(player_name)
        if not player_id:
            print(f"No NBA player found with the name '{player_name}'.")
            return

        teams_played_for = get_teams_player_played_for(player_id)

        if team_one_abv in teams_played_for and team_two_abv in teams_played_for:
            print(f"✅ Yes, {player_name} has played for both teams.")
            score += 1
            print("Your current score is:", score)
        else:
            print(f"❌ No, {player_name} has not played for both teams.")
            print("Your final score is:", score)
            continue_game = False

if __name__ == "__main__":
    main()