import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import sys
import glob

################################
# Begin Connectivity Matrix ####

class LocalOnlyConnectivityMats(object):
    def __init__(self, infile):
        self.name = infile
        srcdat = pd.read_csv(infile)
        self.srcdat = srcdat[(srcdat.EventType == "Pass") &
                             (srcdat.TeamID == 'Huskies') &
                             (srcdat.DestinationPlayerID != None)]
        if(len(self.srcdat) == 0):
            raise AssertionError
        self.idx_to_name = { i:name for i,name in enumerate(self.srcdat['OriginPlayerID'].unique()) }
        self.name_to_idx = { name:i for i,name in enumerate(self.srcdat['OriginPlayerID'].unique()) }

        self.dim = len(self.idx_to_name)
        dim = self.dim

        self.diadjmat = np.zeros((dim,dim), np.int)
        self.uadjmat = np.zeros((dim,dim), np.int)
        for row in self.srcdat.to_dict(orient='records'):
            self.umat_incr(row)
            self.dimat_incr(row)

        self.ueigs = np.linalg.eigvals(self.uadjmat)

    def dimat_incr(self, rrow):
        try:
            res = ( self.name_to_idx[ rrow['OriginPlayerID'] ],
                    self.name_to_idx[ rrow['DestinationPlayerID']])
        except KeyError:
            # This occurs if we have a bad pass, throws this data point away
            return
        self.diadjmat[res] += 1

    def umat_incr(self, rrow):
        try:
            res = ( self.name_to_idx[ rrow['OriginPlayerID'] ],
                    self.name_to_idx[ rrow['DestinationPlayerID']])
        except KeyError:
            # This occurs if we have a bad pass, throws this data point away
            return
        self.uadjmat[res] += 1
        res = ( self.name_to_idx[rrow['DestinationPlayerID']],
                self.name_to_idx[rrow['OriginPlayerID']] )
        self.uadjmat[res] += 1

# End Connectivity Matrix ######
################################


def heatmap(mat: np.array):
    plt.imshow(mat)
    plt.show()

def get_all_mats(pathglob):
    infiles = glob.glob(pathglob)
    mats = []
    for inputfile in infiles:
        try:
            M = LocalOnlyConnectivityMats(inputfile)
            mats.append(M)
        except AssertionError:
            print(f"Play {inputfile} has no passes for our team")
            pass
    return mats


def heats(ms):
     for b in ms:
         plt.imshow(b.uadjmat)
         plt.imshow(b.diadjmat)
         plt.show()

def plots(ms):
    for b in ms:
        plt.plot(b.uadjmat)
        plt.plot(b.diadjmat)
        plt.show()

# v = get_all_mats("data/plays/play??")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        infiles = 'data/huskiespassingevents.csv'
    else:
        infiles = sys.argv[1]
    mats = get_all_mats(infiles)
    # heatmap(M.diadjmat)
    # heatmap(M.uadjmat)

