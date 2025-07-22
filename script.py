from nba_api.stats.static import players, teams
import time
from nba_api.stats.endpoints import playercareerstats
import random

team_abvs = ['1610612737', '1610612738', '1610612751', '1610612766', '1610612741', '1610612739', '1610612742', '1610612743',
             '1610612765', '1610612744', '1610612745', '1610612754', '1610612746', '1610612747', '1610612763', '1610612748',
             '1610612749', '1610612750', '1610612752', '1610612740', '1610612760', '1610612753', '1610612755', '1610612756',
             '1610612757', '1610612758', '1610612759', '1610612761', '1610612762', '1610612764']

all_players = players.get_players()
player_names = [p['full_name'] for p in all_players]

def get_player_id(player_name):
    for player in all_players:
        if player_name.lower() == player['full_name'].lower():
            return player['id']
    return None

def get_teams_player_played_for(player_id):
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    time.sleep(0.6)
    df = career.get_data_frames()[0]
    return df

def main():
    player_id = get_player_id("Tim Duncan")
    teams_played_for = get_teams_player_played_for(player_id)
    print(teams_played_for)

    player_id = get_player_id("Vince Carter")
    teams_played_for = get_teams_player_played_for(player_id)
    print(teams_played_for)

    player_id = get_player_id("John Stockton")
    teams_played_for = get_teams_player_played_for(player_id)
    print(teams_played_for)

    player_id = get_player_id("John Wall")
    teams_played_for = get_teams_player_played_for(player_id)
    print(teams_played_for)

if __name__ == "__main__":
    main()