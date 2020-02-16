import pandas as pd
import numpy as np

from readplay import read_glob_of_plays

import inspect

################################
# Begin Connectivity Matrix ####
valid_passes = [
    "Cross",
    "Hand pass",
    "Head pass",
    "High pass",
    "Launch",
    "Simple pass",
    "Smart pass"
]

team = "Huskies"

def filter_event(event):
    return event['EventSubType'] in valid_passes \
           and team == event["TeamID"] \
           and event['DestinationPlayerID'] != float("NaN")

def get_playerids(filepath):
    f = open(filepath)
    return [x.strip() for x in f.readlines()]

def big_dimat_df(play : dict):
    """ IMPORTANT: FILTER TO MAKE MATRIX """
    play = [event for event in play if filter_event(event)]

    playerids = get_playerids(f"data/playerfiles/{team}_players.txt")
    dim = len(playerids)
    dimat = pd.DataFrame(data=np.zeros((dim,dim), np.int),columns=playerids, index=playerids, dtype=int)
    for passing_event in play:
        try:
            res = ( passing_event['OriginPlayerID'],
                    passing_event['DestinationPlayerID'])
            dimat[res[0]][res[1]] += 1
        except (TypeError, KeyError):
            pass
    return dimat

def big_umat_df(play : dict):
    """ IMPORTANT: FILTER TO MAKE MATRIX """
    play = [event for event in play if filter_event(event)]

    playerids = get_playerids(f"data/playerfiles/{team}_players.txt")
    dim = len(playerids)
    umat = pd.DataFrame(data=np.zeros((dim,dim), np.int),columns=playerids, index=playerids, dtype=int)

    for passing_event in play:
        try:
            res = (passing_event['OriginPlayerID'],
                   passing_event['DestinationPlayerID'])
            umat[res[0]][res[1]] += 1
            res = (passing_event['DestinationPlayerID'],
                   passing_event['OriginPlayerID'])
            umat[res[0]][res[1]] += 1
        except (TypeError, KeyError):
            pass
    return umat

def largest_eig_value(df : pd.DataFrame):
    return np.max(np.linalg.eigvals(np.array(df)))

def evan_call_this_for_eigs(play : dict):
    return largest_eig_value(big_umat_df(play))

def laplacian(play : dict):
    """ calculate the laplacian matrix
    L = D - A
    D is the degree matrix
    """
    A = np.array(big_umat_df(play))
    temp = np.array(big_dimat_df(play))
    degrees = np.sum(temp, 0)
    print(degrees)
    dim = len(A[0])
    D = np.zeros((dim,dim), np.int)
    D[A != 0] = -1
    for i in range(dim):
        D[i][i] = degrees[i]

    L = D - A
    return L

def algebraic_connectivity(play : dict):
    """ return the second smallest eigen value of the laplacian of the connectivity matrix """
    L = laplacian(play)
    return np.sort(np.linalg.eigvals(np.array(L)))[-2]

if __name__ == '__main__':
    paths = "data/plays/play000?H"
    plays = read_glob_of_plays(paths)

    for p in plays:
        print(algebraic_connectivity(p))

    # for p in plays:
    #     res = big_umat_df(p)
    #     print(largest_eig_value(res))

