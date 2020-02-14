import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import ipdb

fdata = pd.read_csv("data/fullevents.csv")
mdat = pd.read_csv("data/matches.csv")
pdat = pd.read_csv("data/passingevents.csv")
hpdat = pd.read_csv("data/huskiespassingevents.csv")

# pass matrix, game by game
srcdat = hpdat

# filter out only our players
idx_to_name = { i:name for i,name in enumerate(srcdat['OriginPlayerID'].unique()) }
name_to_idx = { name:i for i,name in enumerate(srcdat['OriginPlayerID'].unique()) }

dim = len(idx_to_name)

adjmat = np.zeros((dim,dim))

def dimat_idexs(row):
    ipdb.set_trace()
    res = ( name_to_idx[ row['OriginPlayerID'] ],
            name_to_idx[ row['DestinationPlayerID']])
    return res


for row in hpdat.values[:10]:
    res = dimat_idexs(row)
    print(res)
    adjmat[ res ] += 1

