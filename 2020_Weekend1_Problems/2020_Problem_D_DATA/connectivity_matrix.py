import pandas as pd
import numpy as np

import networkx as nx

from readplay import read_glob_of_plays
from globals import *


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

def filter_event(event):
    return event['EventSubType'] in valid_passes \
           and team == event["TeamID"] \
           and event['DestinationPlayerID'] != float("NaN")

def drop_non_active_players(df : pd.DataFrame):
    a = df.loc[(df!=0).any(axis=1)]
    a = a.loc[:, (a.T!=0).any(axis=1)]
    return a

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

def local_umat_df(play : dict):
    df = big_umat_df(play)
    res = drop_non_active_players(df)
    return res

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
    dim = len(A[0])
    D = np.zeros((dim,dim), np.int)
    D[A != 0] = -1
    for i in range(dim):
        D[i][i] = degrees[i]

    L = D - A
    return L

def normalized_laplacian(play : dict):
    G = nx.Graph(big_umat_df(play))
    res = nx.normalized_laplacian_matrix(G)
    return res

def normalized_laplacian_spectrum(play : dict):
    G = nx.Graph(big_umat_df(play))
    res = nx.normalized_laplacian_spectrum(G)
    return res

def directed_laplacian(play: dict):
    raise NotImplementedError

def algebraic_connectivity(play : dict):
    """ return the second smallest eigen value of the laplacian of the connectivity matrix """
    L = laplacian(play)
    return np.sort(np.linalg.eigvals(np.array(L)))[-2]

def nx_algebraic_connectivity(play : dict):
    """ return the second smallest eigen value of the laplacian of the connectivity matrix """
    df = local_umat_df(play)
    G = nx.Graph(df)
    return nx.algebraic_connectivity(G)

def normalized_algebraic_connectivity(play : dict):
    """ return the second smallest eigen value of the laplacian of the connectivity matrix """
    df = local_umat_df(play)
    G = nx.Graph(df)
    return nx.algebraic_connectivity(G, normalized=True)

def degree_centrality(play : dict):
    G = nx.Graph(big_umat_df(play))
    res = nx.degree_centrality(G)
    res = {x : res[x] for x in res if res[x] != 0}
    return res

def closeness_centrality(play : dict):
    G = nx.Graph(big_umat_df(play))
    res = nx.closeness_centrality(G)
    res = {x : res[x] for x in res if res[x] != 0}
    return res

def betweenness_centrality(play : dict):
    G = nx.Graph(big_umat_df(play))
    res = nx.betweenness_centrality(G)
    res = {x : res[x] for x in res if res[x] != 0}
    return res

def nx_spectral_layout(play : dict):
    G = nx.Graph(big_umat_df(play))
    return nx.spectral_layout(G)

def triadic_census(play : dict):
    DG = nx.DiGraph(big_dimat_df(play))
    res = nx.triadic_census(DG)
    return res

def network_simplex(play : dict):
    DG = nx.DiGraph(big_dimat_df(play))
    res = nx.network_simplex(DG)
    return res

diad = "102"
weak_triads = [
    "111D",
    "021D",
    "111U",
    "021U",
    "030T",
    "021C"
]
playmakers_triad = "120D" # really just a weak triad
greedy_striker_triad = "120U"
# strong triads are strongly connected
strong_triads = [
    "201",
    "210",
    "300",
    "030C",
    "120C"
]

def triad_sum(play : dict):
    """ sum the strong triads """
    ts = triadic_census(play)
    res = [ts[t] for t in strong_triads]
    return sum(res)

def diadic_sum(play : dict):
    """ sum of diads """
    ds = triadic_census(play)
    res = ds[diad]
    return res

if __name__ == '__main__':
    paths = "data/games/game*"
    plays = read_glob_of_plays(paths)

    for p in plays:
        # print(algebraic_connectivity(p))
        # print(degree_centrality(p))
        # print(closeness_centralit(p))
        # print(betweenness_centrality(p))
        # print(triadic_census(p)['300'])
        # print(normalized_laplacian_spectrum(p))
        print("========================================")
        print(normalized_algebraic_connectivity(p) )
        print(nx_algebraic_connectivity(p))
        print(triad_sum(p))


    # for p in plays:
    #     res = big_umat_df(p)
    #     print(largest_eig_value(res))

