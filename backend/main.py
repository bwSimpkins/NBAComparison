from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats, teamdetails, commonteamroster
from typing import Dict
import time

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

nba_teams = teams.get_teams()
team_dict = {team['id']: team for team in nba_teams}

@app.get("/teams")
def get_teams():
    return nba_teams

@app.get("/compare")
def compare_teams(team1_id: int = Query(...), team2_id: int = Query(...)) -> Dict:
    def get_team_stats(team_id):
        # Slow down to avoid being rate-limited by NBA API
        time.sleep(1)

        team_info = team_dict.get(team_id)
        if not team_info:
            return None

        # Championships (from year-by-year results)
        stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id).get_data_frames()[0]
        championships = stats[(stats['LEAGUE_ID'] == '00') & (stats['WL_PCT'] == 1.0)].shape[0]

        # Roster for All-Star estimates (simplified)
        current_year = stats.iloc[-1]["YEAR"]
        roster = commonteamroster.CommonTeamRoster(team_id=team_id).get_data_frames()[0]
        all_star_count = len(roster)  # Placeholder: you could enhance this with player history

        return {
            "name": team_info["full_name"],
            "championships": championships,
            "all_stars": all_star_count,
            "head_to_head_wins": 0  # Placeholder – real head-to-head data requires more logic
        }

    team1_data = get_team_stats(team1_id)
    team2_data = get_team_stats(team2_id)

    return {
        "team1": team1_data,
        "team2": team2_data
    }
