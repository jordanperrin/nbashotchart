from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail

import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from matplotlib.path import Path
from matplotlib.patches import PathPatch


app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/shotchart_data/<player_name>/<season_id>", methods=['GET'])
def hotchart_data(player_name, season_id):
    nba_players =  players.get_players()
    player_dict = [player for player in nba_players if player['full_name'].lower() == player_name][0]

    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    #data frame
    career_df = career.get_data_frames()[0]

    #following the nba api for datashotchart endpoint we need the team id and the player id
    #get the team id for that season
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']

    shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id), 
                                                    player_id = int(player_dict['id']),
                                                    season_type_all_star = 'Regular Season',
                                                    season_nullable = season_id,
                                                    context_measure_simple = "FGA").get_data_frames()


    return shotchartlist[0], shotchartlist[1]


def draw_court(ax=None, color="blue", lw=1, outer_lines=False):
    
    if ax is None:
        ax = plt.gca()

    hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)

    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    court_elements = [hoop]

    for element in court_elements:
        ax.add_patch(element)


if __name__ == "__main__":
    while(True):
        xlim= (-250, 250)
        ylim= (422.5, -47.5)

        ax = plt.gca()
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

        draw_court(ax)
        plt.show()