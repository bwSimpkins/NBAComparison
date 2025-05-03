import pandas as pd
import requests
from bs4 import BeautifulSoup


def main():
    # url where head to head data is contained
    base_url = 'https://www.basketball-reference.com/teams/{}/head2head.html'

    # Data frame containing Team names and df to store head 2 head results
    teams = ['ATL', 'BOS', 'NJN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA',
             'MIL', 'MIN', 'NYK', 'NOH', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

    teams_names = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls',
                   'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors',
                   'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
                   'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New York Knicks', 'New Orleans Pelicans',
                   'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trailblazers',
                   'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']

    for team in teams_names:

        # Loop that iterates through each teams webpage and grabs their head2head table
        index = 0
        for name in teams_names:
            if first_team == name:
                team = teams[index]
            index += 1

        try:
            # Inserting the specified team name into the base URL
            req_url = base_url.format(team)

            # Grabs the web page of interest
            req = requests.get(req_url)
            soup = BeautifulSoup(req.content, 'html.parser')

            # Searches for table with the ID tag that is universal to each team's head to head page and saves it to a df
            table = soup.find('table', {'id': 'head2head'})
            df = pd.read_html(str(table))[0]

            # Finds second team in data frame
            df = df.iloc[:, 1:]
            df = df[df['Franchise'] == second_team]

            print(df)

            wins = df.iloc[0]['W']
            losses = df.iloc[0]['L']
            win_percentage = df.iloc[0]['W/L%']

            print("The", first_team, "are", wins, "and", losses, "against the", second_team,
                  "resulting in a win percentage of", win_percentage)

        except ValueError:
            print("oops! No data on: " + first_team)

main()