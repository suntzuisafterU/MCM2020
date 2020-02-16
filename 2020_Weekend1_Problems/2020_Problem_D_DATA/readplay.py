
import pandas as pd
import glob

def readplay(path):
    
    f = open(path)

    data = pd.read_csv(path)

    return data.values

def read_spectral_play(path):
    f = open(path)

    data = pd.read_csv(path)
    data = data[(data.EventSubType == "Cross") | (data.EventSubType == "Hand pass") | (
            data.EventSubType == "Head pass") | (data.EventSubType == "High pass") | (
                            data.EventSubType == "Launch") | (data.EventSubType == "Simple pass") | (
                            data.EventSubType == "Smart pass") |
                    (data.TeamID == 'Huskies') &
                    (data.DestinationPlayerID != float("NaN"))]
    if len(data) == 0:
        return None

    return data.to_dict(orient='records')


def give_me_plays_as_list(pathglob):
    paths = glob.glob(pathglob)

    res = []
    for filepath in paths:
        res.append(readplay(filepath))

    return res

def give_me_spectral_dicts(pathglob):
    paths = glob.glob(pathglob)

    res = []
    for filepath in paths:
        res.append(read_spectral_play(filepath))

    return res

def lists_and_spectral_dicts(pathglob):
    lists = give_me_plays_as_list(pathglob)
    dicts = give_me_spectral_dicts(pathglob)
    return zip(lists, dicts)
