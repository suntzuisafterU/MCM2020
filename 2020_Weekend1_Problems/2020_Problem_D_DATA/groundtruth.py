import sys
import ntpath

from readplay import *
import playGraph as pg

import numpy as np

from globals import *

def play_to_np_array(play):
    return np.array([[event[key] for key in event] for event in play])

offense_markers = {
    "Shot": 1.0,
    "Cross": 0.5
}

def _ground_truth_offense(play):
    # sum shots and crosses with scalar
    value = 0
    for event in play:
        for key, scalar in offense_markers.items():
            if event["TeamID"] == team and event["EventSubType"] == key:
                value += scalar
    return value

our_team_defensive_markers = {
    "Clearance": 0.5,
    "Ground loose ball duel": 0.1,
    "Air duel": 0.1,
    "Ground defending duel": 0.3
}

opponent_team_defensive_markers = {
    "Shot": -1.0
}

def _ground_truth_defense(play):
    # sum shots and crosses with scalar
    value = 0
    for event in play:
        for key, scalar in our_team_defensive_markers.items():
            if event["TeamID"] == team and event["EventSubType"] == key:
                value += scalar
        for key, scalar in opponent_team_defensive_markers.items():
            if event["TeamID"] != team and event["EventSubType"] == key:
                value += scalar
    return value

def ground_truth(play):
    return _ground_truth_offense(play) + _ground_truth_defense(play)

def calc_offensive_groundtruth_plays():
    playglob = "data/plays/play*"
    play_paths = glob.glob(playglob)
    play_values = []
    for path in play_paths:
        basename = ntpath.basename(path)
        play = readplay(path)
        play_values.append(f"{basename}, {_ground_truth_offense(play)}\n")
    f = open("data/groundtruths/playoffenseivegroundtruths.csv", "w")
    f.writelines(play_values)

def calc_offensive_groundtruth_games():
    gameglob = "data/games/game*"
    game_paths = glob.glob(gameglob)
    game_values = []
    for path in game_paths:
        basename = ntpath.basename(path)
        game = readplay(path)
        game_values.append(f"{basename}, {_ground_truth_offense(game)}\n")
    f = open("data/groundtruths/game_offensive_groundtruths.csv", "w")
    f.writelines(game_values)

def calc_defensive_groundtruth_plays():
    playglob = "data/plays/play*"
    play_paths = glob.glob(playglob)
    play_values = []
    for path in play_paths:
        basename = ntpath.basename(path)
        play = readplay(path)
        play_values.append(f"{basename}, {_ground_truth_offense(play)}\n")
    f = open("data/groundtruths/play_offenseive_groundtruths.csv", "w")
    f.writelines(play_values)

def calc_defensive_groundtruth_games():
    gameglob = "data/games/game*"
    game_paths = glob.glob(gameglob)
    game_values = []
    for path in game_paths:
        basename = ntpath.basename(path)
        game = readplay(path)
        game_values.append(f"{basename}, {_ground_truth_offense(game)}\n")
    f = open("data/groundtruths/game_offensive_groundtruths.csv", "w")
    f.writelines(game_values)

if __name__ == "__main__":
    calc_offensive_groundtruth_plays()
    calc_offensive_groundtruth_games()
    calc_defensive_groundtruth_plays()
    calc_defensive_groundtruth_games()

