import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import sys
import glob

################################
# Begin Connectivity Matrix ####

class ConnectivityMats(object):
    def __init__(self, infile):
        srcdat = pd.read_csv(infile)
        self.srcdat = srcdat[(srcdat.EventType == "Pass") & (srcdat.TeamID == 'Huskies')]
        self.idx_to_name = { i:name for i,name in enumerate(self.srcdat['OriginPlayerID'].unique()) }
        self.name_to_idx = { name:i for i,name in enumerate(self.srcdat['OriginPlayerID'].unique()) }

        self.dim = len(self.idx_to_name)
        dim = self.dim

        self.diadjmat = np.zeros((dim,dim), np.int)
        self.uadjmat = np.zeros((dim,dim), np.int)
        for row in self.srcdat.to_dict(orient='records'):
            self.umat_incr(row)
            self.dimat_incr(row)

    def dimat_incr(self, rrow):
        res = ( self.name_to_idx[ rrow['OriginPlayerID'] ],
                self.name_to_idx[ rrow['DestinationPlayerID']])
        self.diadjmat[res] += 1

    def umat_incr(self, rrow):
        res = ( self.name_to_idx[ rrow['OriginPlayerID'] ],
                self.name_to_idx[ rrow['DestinationPlayerID']])
        self.uadjmat[res] += 1
        res = ( self.name_to_idx[rrow['DestinationPlayerID']],
                self.name_to_idx[rrow['OriginPlayerID']] )
        self.uadjmat[res] += 1

# End Connectivity Matrix ######
################################




def heatmap(mat: np.array):
    plt.imshow(mat)
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        infiles = ['data/huskiespassingevents.csv']
    else:
        infiles = glob.glob(sys.argv[1])
    for inputfile in infiles:
        M = ConnectivityMats(inputfile)
        # heatmap(M.diadjmat)
        heatmap(M.uadjmat)


