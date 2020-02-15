
import pandas as pd
import glob

def readplay(path):
    
    f = open(path)

    data = pd.read_csv(path)

    return data.values

def read_a_play_for_spectral_passing_adj_mats(path):
    f = open(path)

    data = pd.read_csv(path)
    data = data[(data.EventSubType == "Cross") | (data.EventSubType == "Hand pass") | (
            data.EventSubType == "Head pass") | (data.EventSubType == "High pass") | (
                            data.EventSubType == "Launch") | (data.EventSubType == "Simple pass") | (
                            data.EventSubType == "Smart pass") |
                    (data.TeamID == 'Huskies') &
                    (data.DestinationPlayerID != None)]

    return data.to_dict(orient='records')


def read_a_set_of_plays(pathglob):
    paths = glob.glob(pathglob)

    res = []
    for filepath in paths:
        res.append(readplay(filepath))

    return res

