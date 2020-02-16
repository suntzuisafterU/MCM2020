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
    dat = play_to_np_array(play)
    value = 0
    for d in dat:
        for key, scalar in offense_markers.items():
            if d[7] == key:
                value += scalar
    return value


if __name__ == "__main__":
    playglob = "data/plays/play*"
    play_paths = glob.glob(playglob)
    play_values = []
    for path in play_paths:
        # TODO: could use basename if easier
        basename = ntpath.basename(path)
        play = readplay(path)
        play_values.append(f"{basename}, {ground_truth_offense(play)}\n")
    f = open("data/groundtruths/playgroundtruths.csv", "w")
    f.writelines(play_values)

    gameglob = "data/games/game*"
    game_paths = glob.glob(gameglob)
    game_values = []
    for path in game_paths:
        # TODO: could use basename if easier
        basename = ntpath.basename(path)
        game = readplay(path)
        game_values.append(f"{basename}, {ground_truth_offense(game)}\n")
    f = open("data/groundtruths/gamegroundtruths.csv", "w")
    f.writelines(game_values)

