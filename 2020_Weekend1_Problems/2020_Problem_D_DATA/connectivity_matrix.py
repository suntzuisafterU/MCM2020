import pandas as pd
import numpy as np

import networkx as nx

from readplay import read_glob_of_plays
from globals import *



def accept_invalid_network(func):
    def wrapper(play):
        try:
            return func(play)
        except nx.NetworkXError:
            return 0
    wrapper.__name__ = func.__name__
    return wrapper


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

def filter_event_dont_touch(event):
    return event['EventSubType'] in valid_passes \
           and team != event["TeamID"] \
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

@accept_invalid_network
def defensive_damage2(play : dict):
    df = mat_with_duel_cons(play)
    res = drop_non_active_players(df)

    global team
    orig_team = team
    team = this_opp(play)
    algcon = nx_algebraic_connectivity(play)
    G = nx.Graph(res)
    team = orig_team

    res = nx.algebraic_connectivity(G)
    if res == 0:
        return 0
    return res - algcon

@accept_invalid_network
def defensive_damage3(play: dict):
    df = mat_with_duel_cons2(play)
    res = drop_non_active_players(df)

    global team
    orig_team = team
    team = this_opp(play)
    algcon = nx_algebraic_connectivity(play)
    team = orig_team

    G = nx.Graph(res)
    res = nx.algebraic_connectivity(G)
    if res == 0:
        return 0
    return res - algcon

@accept_invalid_network
def defensive_damage4(play : dict):
    df = mat_with_duel_cons(play)
    res = drop_non_active_players(df)
    G = nx.Graph(res)
    return nx.algebraic_connectivity(G)

@accept_invalid_network
def defensive_damage5(play: dict):
    df = mat_with_duel_cons2(play)
    res = drop_non_active_players(df)
    G = nx.Graph(res)
    return nx.algebraic_connectivity(G)

def this_opp(play: dict):
    thisgame = this_game(play)
    thisopp = "?"
    fiiil = open("data/matches.csv", "r")
    fiiil.readline()
    for f in fiiil:
        x = f.split(",")
        if int(x[0]) == thisgame:
            if team == "Huskies":
                thisopp = x[1]
            else:
                thisopp = "Huskies"
            break
    return thisopp

def this_game(play : dict):
    return play[0]["MatchID"]

def mat_with_duel_cons(play: dict):
    #playerids = get_playerids(f"data/playerfiles/all_players.txt")
    thisgame = this_game(play)

    thisopp = this_opp(play)

    playerids = get_playerids(f"data/playerfiles/{thisopp}_players.txt")
    playerids += get_playerids(f"data/playerfiles/{team}_players.txt")
    if thisgame == 26:
        playerids += ["Opponent5_M3"]
    if thisgame == 33:
        playerids += ["Opponent13_D1"]
    if thisgame == 34:
        playerids += ["Opponent14_F2"]

    dim = len(playerids)
    umat = pd.DataFrame(data=np.zeros((dim, dim), np.int), columns=playerids, index=playerids, dtype=int)

    passes = [event for event in play if filter_event_dont_touch(event)]
    for passing_event in passes:
        try:
            res = (passing_event['OriginPlayerID'],
                   passing_event['DestinationPlayerID'])
            umat[res[0]][res[1]] += 1
            res = (passing_event['DestinationPlayerID'],
                   passing_event['OriginPlayerID'])
            umat[res[0]][res[1]] += 1
        except (TypeError, KeyError):
            pass

    for i in range(len(play) - 1):
        if play[i]["EventType"] == "Duel" and play[i + 1]["EventType"] == "Duel":
            res = (play[i]["OriginPlayerID"], play[i + 1]["OriginPlayerID"])
            umat[res[0]][res[1]] += 1
            umat[res[1]][res[0]] += 1
    return umat



# does it without adding adverserial passing edges
def mat_with_duel_cons2(play: dict):
    #playerids = get_playerids(f"data/playerfiles/all_players.txt")

    thisgame = this_game(play)
    thisopp = this_opp(play)
    playerids = get_playerids(f"data/playerfiles/{thisopp}_players.txt")
    playerids += get_playerids(f"data/playerfiles/{team}_players.txt")
    if thisgame == 26:
        playerids += ["Opponent5_M3"]
    if thisgame == 33:
        playerids += ["Opponent13_D1"]
    if thisgame == 34:
        playerids += ["Opponent14_F2"]

    dim = len(playerids)
    umat = pd.DataFrame(data=np.zeros((dim, dim), np.int), columns=playerids, index=playerids, dtype=int)

    passes = [event for event in play if filter_event_dont_touch(event)]
    for passing_event in passes:
        try:
            if passing_event["TeamID"] == thisopp:
                res = (passing_event['OriginPlayerID'],
                       passing_event['DestinationPlayerID'])
                umat[res[0]][res[1]] += 1
                res = (passing_event['DestinationPlayerID'],
                       passing_event['OriginPlayerID'])
                umat[res[0]][res[1]] += 1
            else:
                raise AssertionError
        except (TypeError, KeyError):
            pass

    for i in range(len(play) - 1):
        if play[i]["EventType"] == "Duel" and play[i + 1]["EventType"] == "Duel":
            res = (play[i]["OriginPlayerID"], play[i + 1]["OriginPlayerID"])
            umat[res[0]][res[1]] += 1
            umat[res[1]][res[0]] += 1
    return umat


def defensive_damage(play : dict):
    df = poison_umat(play)
    G = nx.Graph(df)
    return nx.algebraic_connectivity(G) * 10


def duels_umat(play: dict):
    #playerids = get_playerids(f"data/playerfiles/all_players.txt")

    thisgame = play[0]["MatchID"]
    thisopp = "?"
    fiiil = open("data/matches.csv", "r")
    fiiil.readline()
    for f in fiiil:
        x = f.split(",")
        if int(x[0]) == thisgame:
            if team == "Huskies":
                thisopp = x[1]
            else:
                thisopp = "Huskies"
            break


    playerids = get_playerids(f"data/playerfiles/{thisopp}_players.txt")
    playerids += get_playerids(f"data/playerfiles/{team}_players.txt")
    if thisgame == 26:
        playerids += ["Opponent5_M3"]
    if thisgame == 33:
        playerids += ["Opponent13_D1"]
    if thisgame == 34:
        playerids += ["Opponent14_F2"]

    dim = len(playerids)
    umat = pd.DataFrame(data=np.zeros((dim, dim), np.int), columns=playerids, index=playerids, dtype=int)

    for i in range(len(play) - 1):

        if play[i]["EventType"] == "Duel" and play[i + 1]["EventType"] == "Duel":
            res = (play[i]["OriginPlayerID"], play[i + 1]["OriginPlayerID"])
            umat[res[0]][res[1]] += 1
            umat[res[1]][res[0]] += 1
    return umat



# weighted adj mat
def local_umat_df(play : dict):
    df = big_umat_df(play)
    res = drop_non_active_players(df)
    return res

def ddddddddddddd(infile):
    playerids = get_playerids(f"data/playerfiles/all_players.txt")
    idx_to_name = {i:name for i,name in enumerate(playerids)}
    name_to_idx = {name:i for i,name in enumerate(playerids)}

    dim = len(idx_to_name)
    uadjmat = np.zeros((dim,dim), np.int)


def poison_def_met(play : dict):
    """ IMPORTANT: FILTER TO MAKE MATRIX """


    playerids = get_playerids(f"data/playerfiles/all_players.txt")
    dim = len(playerids)
    umat = pd.DataFrame(data=np.zeros((dim,dim), np.int),columns=playerids, index=playerids, dtype=int)

    for passing_event in play:
        try:
            if passing_event["EventSubType"] == "Ground defending duel" and passing_event['TeamID'] == team:
                res = passing_event['OriginPlayerID']
                for player in playerids:
                    if umat[res][player] > 1:
                        umat[res][player] -= 1
                    if umat[player][res] > 1:
                        umat[player][res] -= 1
            if passing_event["EventType"] == "Pass" and passing_event['TeamID'] == team:
                res = (passing_event['OriginPlayerID'],
                     passing_event['DestinationPlayerID'])
                umat[res[0]][res[1]] += 1
                umat[res[1]][res[0]] += 1

        except (TypeError, KeyError):
            pass
    return umat





def poison_umat(play : dict):
    df = duels_umat(play)
    res = drop_non_active_players(df)
    return res


def largest_eig_value(df : pd.DataFrame):
    return np.max(np.linalg.eigvals(np.array(df)))

def network_strength_eigen_value(play : dict):
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

@accept_invalid_network
def nx_algebraic_connectivity(play : dict):
    """ return the second smallest eigen value of the laplacian of the connectivity matrix """
    df = local_umat_df(play)
    G = nx.Graph(df)
    return nx.algebraic_connectivity(G)

@accept_invalid_network
def normalized_algebraic_connectivity(play : dict):
    """ return the second smallest eigen value of the laplacian of the connectivity matrix """
    df = local_umat_df(play)
    G = nx.Graph(df)
    return nx.algebraic_connectivity(G, normalized=True)

@accept_invalid_network
def defensive_damage(play : dict):
    df = poison_umat(play)
    G = nx.Graph(df)
    return nx.algebraic_connectivity(G) * 10

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

def min_cut_value(play : dict):
    raise NotImplementedError
    DG = nx.DiGraph(big_dimat_df(play))
    res = nx.minimum_cut_value(DG)

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

complete_triad = "300"

def complete_triad_sum(play : dict):
    ts = triadic_census(play)
    res = ts[complete_triad]
    print(res)
    return res

def triad_sum(play : dict):
    """ sum the strong triads """
    ts = triadic_census(play)
    res = [ts[t] for t in strong_triads]
    print(res)
    return sum(res)

def diadic_sum(play : dict):
    """ sum of diads """
    ds = triadic_census(play)
    res = ds[diad]
    return res

def extract_all_triads(play : dict):
    DG = nx.DiGraph(big_dimat_df(play))
    ds = nx.triadic_census(DG)


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
        # print(normalized_algebraic_connectivity(p) )
        # print(nx_algebraic_connectivity(p))
        # print(poison_umat(p))
        #print(algebraic_connectivity(p))
        print(triad_sum(p))
        print(complete_triad_sum(p))
        # print(defensive_damage2(p))
        # print(defensive_damage3(p))
    # for p in plays:
    #     res = big_umat_df(p)
    #     print(largest_eig_value(res))


