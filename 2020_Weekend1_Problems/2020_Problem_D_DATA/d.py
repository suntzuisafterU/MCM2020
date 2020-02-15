import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

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

diadjmat = np.zeros((dim,dim))
uadjmat = np.zeros((dim,dim))


def dimat_incr(rrow):
    res = ( name_to_idx[ rrow['OriginPlayerID'] ],
            name_to_idx[ rrow['DestinationPlayerID']])
    diadjmat[res] += 1


def umat_incr(rrow):
    res = ( name_to_idx[ rrow['OriginPlayerID'] ],
            name_to_idx[ rrow['DestinationPlayerID']])
    uadjmat[res] += 1
    res = ( name_to_idx[rrow['DestinationPlayerID']],
            name_to_idx[rrow['OriginPlayerID']] )
    uadjmat[res] += 1


for row in hpdat.to_dict(orient='records'):
    umat_incr(row)
    dimat_incr(row)


def heatmap(mat):
    plt.imshow(mat)
    plt.show()


if __name__ == '__main__':
    heatmap(diadjmat)
    heatmap(uadjmat)
