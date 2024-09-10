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

    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color = color, fill = False)

    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color = color, fill = False)

    top_key = Arc((0, 142.5), 120, 120, theta1=0, theta2=360, linewidth=lw, color = color, fill=False)

    restricted = Arc((0,0), 80,80, theta1=0, theta2=180, linewidth=lw, color=color, fill=False )

    #Three Pointer
    corner_three_right = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color) 
    corner_three_left = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color) 

    three_arc = Arc((0,0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    #HalfCourt
    center_outer_arc = Arc((0,422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    inner_outer_arc = Arc((0,422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)


    court_elements = [hoop, backboard, outer_box, inner_box, top_key, restricted, corner_three_right, corner_three_left,three_arc,center_outer_arc, inner_outer_arc]

    outer_lines = True

    if outer_lines:
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill = False)
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)


if __name__ == "__main__":
   
    xlim= (-250, 250)
    ylim= (422.5, -47.5)

    ax = plt.gca()
    ax.set_xlim(xlim[::-1])
    ax.set_ylim(ylim[::-1])

    draw_court(ax)
    
    plt.show()