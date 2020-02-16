import pandas as pd
import numpy as np

from readplay import give_me_spectral_dicts

import inspect


################################
# Begin Connectivity Matrix ####

def get_playerids(filepath):
    f = open(filepath)
    return [x.strip() for x in f.readlines()]

def dimat_incr():
    frame = inspect.currentframe().f_back.f_locals
    passing_event = frame.passing_event
    dmat = frame.dmat
    try:
        res = ( passing_event['OriginPlayerID'],
                passing_event['DestinationPlayerID'])
        dmat[res[0]][res[1]] += 1
    except KeyError:
        assert (False, "Why are we here?")
        # This occurs if we have a bad pass, throws this data point away
        return

def big_umat_df(play, team):
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

def largest_eig_value(df):
    return np.max(np.linalg.eigvals(np.array(df)))

def evan_call_this_for_eigs(play):
    team = "Huskies"
    return largest_eig_value(big_umat_df(play, team))


if __name__ == '__main__':
    paths = "data/plays/play000?H"
    plays = give_me_spectral_dicts(paths)

    for p in plays:
        res = big_umat_df(p, "Huskies")
        print(largest_eig_value(res))

