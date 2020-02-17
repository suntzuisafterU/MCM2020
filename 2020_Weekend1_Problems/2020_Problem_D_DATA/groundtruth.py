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

def ground_truth_offense(play):
    # sum shots and crosses with scalar
    value = 0
    for event in play:
        for key, scalar in offense_markers.items():
            if event["TeamID"] == team and event["EventSubType"] == key:
                value += scalar
    return value

our_team_defensive_markers = {
    "Clearance":  0.5
}

opponent_team_defensive_markers = {
    # "Shot": -1.0
}

team_defensive_duel_markers = {
    "Ground loose ball duel": 0.1,
    "Air duel": 0.1,
    "Ground defending duel": 0.3
}

def ground_truth_defense(play : list):
    # sum shots and crosses with scalar
    value = 0
    last_passer = None
    for event in reversed(play):
        if event["EventType"] == "Pass":
            last_passer = event['TeamID']
        for key, scalar in our_team_defensive_markers.items():
            if event["TeamID"] == team and event["EventSubType"] == key:
                value += scalar
        for key, scalar in opponent_team_defensive_markers.items():
            if event["TeamID"] != team and event["EventSubType"] == key:
                value += scalar
        for key, scalar in team_defensive_duel_markers.items():
            if event["TeamID"] == team and last_passer == team:
                value += scalar

    return value

def ground_truth(play):
    return ground_truth_offense(play) + ground_truth_defense(play)

def calc_offensive_groundtruth_plays():
    playglob = "data/plays/play*"
    play_paths = glob.glob(playglob)
    header = f"MatchID,TeamID,GroundTruth\n"
    play_values = [header]
    for path in play_paths:
        basename = ntpath.basename(path)
        play = readplay(path)
        play_values.append(f"{basename},{team},{ground_truth_offense(play)}\n")
    f = open(f"data/groundtruths/play_{team}_offensive_groundtruths.csv", "w")
    f.writelines(play_values)

def calc_offensive_groundtruth_games():
    gameglob = "data/games/game*"
    game_paths = glob.glob(gameglob)
    header = f"MatchID,TeamID,GroundTruth\n"
    game_values = [header]
    for path in game_paths:
        basename = ntpath.basename(path)
        game = readplay(path)
        game_values.append(f"{basename},{team},{ground_truth_offense(game)}\n")
    f = open(f"data/groundtruths/game_{team}_offensive_groundtruths.csv", "w")
    f.writelines(game_values)

def calc_defensive_groundtruth_plays():
    playglob = "data/plays/play*"
    play_paths = glob.glob(playglob)
    header = f"MatchID,TeamID,GroundTruth\n"
    play_values = [header]
    for path in play_paths:
        basename = ntpath.basename(path)
        play = readplay(path)
        play_values.append(f"{basename},{team},{ground_truth_offense(play)}\n")
    f = open(f"data/groundtruths/play_{team}_defenseive_groundtruths.csv", "w")
    f.writelines(play_values)

def calc_defensive_groundtruth_games():
    gameglob = "data/games/game*"
    game_paths = glob.glob(gameglob)
    header = f"MatchID,TeamID,GroundTruth\n"
    game_values = [header]
    for path in game_paths:
        basename = ntpath.basename(path)
        game = readplay(path)
        game_values.append(f"{basename},{team},{ground_truth_offense(game)}\n")
    f = open(f"data/groundtruths/game_{team}_defensive_groundtruths.csv", "w")
    f.writelines(game_values)

def calc_groundtruth_games():
    gameglob = "data/games/game*"
    game_paths = glob.glob(gameglob)
    header = f"MatchID,TeamID,GroundTruth\n"
    game_values = [header]
    for path in game_paths:
        basename = ntpath.basename(path)
        game = readplay(path)
        game_values.append(f"{basename},{team},{ground_truth(game)}\n")
    f = open(f"data/groundtruths/game_{team}_groundtruths.csv", "w")
    f.writelines(game_values)

def calc_groundtruth_plays():
    playglob = "data/plays/play*"
    play_paths = glob.glob(playglob)
    header = f"MatchID,TeamID,GroundTruth\n"
    play_values = [header]
    for path in play_paths:
        basename = ntpath.basename(path)
        play = readplay(path)
        play_values.append(f"{basename},{team},{ground_truth(play)}\n")
    f = open(f"data/groundtruths/play_{team}_groundtruths.csv", "w")
    f.writelines(play_values)

if __name__ == "__main__":
    calc_offensive_groundtruth_plays()
    calc_offensive_groundtruth_games()
    calc_defensive_groundtruth_plays()
    calc_defensive_groundtruth_games()
    calc_groundtruth_plays()
    calc_groundtruth_games()

