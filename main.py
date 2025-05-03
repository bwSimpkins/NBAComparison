from pyscript import document
from pyscript import display
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyodide.http import open_url


def main(event):
    first_team = document.querySelector("#team1")
    output_div = document.querySelector("#team1display")
    
    second_team = document.querySelector("#team2")
    output_div2 = document.querySelector("#team2display")

    first_team = first_team.value
    second_team = second_team.value

    donut_div = document.querySelector("#pie")

    team_colors = ['#e03a3e', '#007a33', '#000000', '#1d1160', '#ce1141', '#860038', '#00538c',
                   '#0e2240', '#c8102e', '#1d428a', '#ce1141', '#002d62', '#c8102e', '#552583',
                   '#5d76a9', '#98002e', '#00471b', '#0c2340', '#006bb6', '#0c2340', '#007ac1',
                   '#0077c0', '#006bb6', '#1d1160', '#e03a3e', '#5a2d81', '#c4ced4', '#ce1141',
                   '#002b5c', '#002b5c']

    if first_team == second_team:
        output_div.innerText = "0 wins"
        output_div2.innerText = "0 wins"

    else:
        first_team = first_team.replace(" ", "%20")
        
        url = 'https://raw.githubusercontent.com/bwSimpkins/TheOppositions/main/' + first_team + '.csv'
        df = pd.read_csv((open_url(url)))
    
        # Find the second team in the data frame
        df = df.iloc[:, 1:]
        df = df[df['Franchise'] == second_team]
    
        wins = df.iloc[0]['W']
        losses = df.iloc[0]['L']
        win_percentage = round(df.iloc[0]['W/L%'] * 100, 1)
        win_percentage2 = round((losses / (wins + losses)) * 100, 1)
    
        output_div.innerText = str(wins) + " Wins: " + str(win_percentage) + "%" 
        output_div2.innerText = str(losses) + " Wins: " + str(win_percentage2) + "%" 

        size_of_groups = [wins, losses]
        teams = [first_team, second_team]
        
        # add a circle at the center to transform it in a donut chart
        my_circle=plt.Circle( (0,0), 0.7, color='white')
        plt.pie(size_of_groups, colors = team_colors)
        donut=plt.gcf()
        donut.gca().add_artist(my_circle)
        donut.set_figwidth(4)
        donut.set_figheight(4)

        display(donut, target="donut", append=False)

        # HIDE PIE CHART LABELS AND RESIZE IN BETWEEN TEAMS
        
        # WOULD LOVE A TABLE OF HEAD-TO-HEAD MATCHUPS

        # MAKE A MAIN MATCHUP PAGE FOR EACH SPORT THAT FEATURES THE GAME
        # WITH THE HIGHEST AVERAGE RATED MATCHUP. OR TEAMS ABOUT TO TAKE
        # A LEAD IN A SERIES

        # BUTTON IS CLICKED WHEN HITTING ENTER

        # ADD LOADING SCREEN
