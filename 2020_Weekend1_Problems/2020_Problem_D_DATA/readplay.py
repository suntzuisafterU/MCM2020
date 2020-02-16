
import pandas as pd
import glob

def readplay(path):
    
    f = open(path)

    data = pd.read_csv(path)

    return data.to_dict(orient='records')

def read_glob_of_plays(pathglob):
    paths = glob.glob(pathglob)

    res = []
    for filepath in paths:
        res.append(readplay(filepath))

    return res

