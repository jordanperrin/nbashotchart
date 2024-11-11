from flask import Flask, request, jsonify, send_file
import io
import json
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
    # players_list =  players.get_players()

    # active_players = [player for player in players_list if player["is_active"] ]
    # file_path = './public/players_data.json'

    # with open(file_path, 'w') as json_file:
    #     json.dump(active_players, json_file, indent=4)
    
    return "<p>Hello, World!</p>"

def get_shotchart_data(player_name, season_id):
    nba_players =  players.get_players()
    player_dict = [player for player in nba_players if player['full_name'].lower() == player_name.lower()][0]

    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    #data frame
    career_df = career.get_data_frames()[0]

    #following the nba api for datashotchart endpoint we need the team id and the player id
    #get the team id for that season
    team_id = career_df[career_df['SEASON_ID'] == season_id]['TEAM_ID']

    print(team_id)

   

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

def shot_chart(data, title="",  color='b', xlim=(-250,250), ylim=(422.5, -47.5), line_color=("blue"), 
                court_color="white", court_lw=2, outer_lines=False, flip_court=False, gridsize=None,
                ax=None, despine=False ):
    if ax is None:
        ax = plt.gca()
    
    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, fontsize=18)

    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
    y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']
   
    x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']


    ax.scatter(x_missed, y_missed, c='r', marker='x', s=100, linewidths=1)
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='g', marker='o', s=100, linewidth=2)


    #set spines to match rest of court lines 

    #makes the line edges of chart wdith and color the same as all the other lines
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    #if despine is true then creates the outer lines invisible
    if despine: 
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)

    return ax

@app.route("/api/shotchart/<player_name>/<season_id>", methods=['GET'])
def get_jpeg(player_name, season_id):
    player_shotchart_df, league_avg = get_shotchart_data(player_name, season_id)

    shot_chart(player_shotchart_df, title="Poop")

    plt.rcParams['figure.figsize'] = (12,11)

    img_buffer = io.BytesIO()

    # Save the plot to the buffer
    plt.savefig(img_buffer, format='jpeg')
    
    # Close the plot to free memory
    plt.close()
    
    # Seek to the beginning of the buffer so the file can be read
    img_buffer.seek(0)
    
    # Send the image as a response with MIME type 'image/jpeg'
    return send_file(img_buffer, mimetype='image/jpeg', as_attachment=False, download_name=f"{player_name}_shotchart.jpeg")



# if __name__ == "__main__":
   
#     player_shotchart_df, league_avg = get_shotchart_data("LeBron James", "2019-20")

#     shot_chart(player_shotchart_df, title="Poop")

#     plt.rcParams['figure.figsize'] = (12,11)

#     plt.show()