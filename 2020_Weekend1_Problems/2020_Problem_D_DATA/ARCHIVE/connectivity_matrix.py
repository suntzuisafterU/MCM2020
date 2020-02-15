import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import sys
import glob

################################
# Begin Connectivity Matrix ####

class Adjmat(object):
    def __init__(self, infile, dim):
        self.name = infile
        self.m = np.zeros((dim,dim), int)

    def calc_eigs(self):
        return np.linalg.eigvals(self.m)

class Uadjmat(Adjmat):
    pass

class Diadjmat(Adjmat):
    pass

########################################################################
### BEGIN ConnectivityMatrixFactory ####################################

class ConnectivityMatrixFactory(object):
    def __init__(self, infile):
        # infile should only be the full dataset
        self.name = infile
        srcdat = pd.read_csv(infile)
        if(len(srcdat) == 0):
            raise AssertionError
        self.idx_to_name = { i:name for i,name in enumerate(srcdat['OriginPlayerID'].unique()) }
        self.name_to_idx = { name:i for i,name in enumerate(srcdat['OriginPlayerID'].unique()) }
        self.dim = len(self.idx_to_name)

    def get_all_mats(self, pathglob):
        infiles = glob.glob(pathglob)
        mats = []
        for inputfile in infiles:
            try:
                M = self.produce_adjmats(inputfile)
                mats.append(M)
            except AssertionError:
                print("Assertion Error???")
                # print(f"Play {inputfile} has no passes for our team")
                pass
        return mats

    def produce_adjmats(self, infile):
        srcdat = pd.read_csv(infile)
        srcdat = srcdat[ (srcdat.EventSubType == "Cross") | (srcdat.EventSubType == "Hand pass") | (srcdat.EventSubType == "Head pass") | (srcdat.EventSubType == "High pass") | (srcdat.EventSubType == "Launch") | (srcdat.EventSubType == "Simple pass") | (srcdat.EventSubType == "Smart pass") |
            (srcdat.TeamID == 'Huskies') &
            (srcdat.DestinationPlayerID != None)]
        dimat = Diadjmat(infile, self.dim)
        umat = Uadjmat(infile, self.dim)
        for row in srcdat.to_dict(orient='records'):
            self.umat_incr(dimat, row)
            self.dimat_incr(umat, row)
        return {"dimat": dimat, "umat": umat}

    def dimat_incr(self, dm, rrow):
        try:
            res = ( self.name_to_idx[ rrow['OriginPlayerID'] ],
                    self.name_to_idx[ rrow['DestinationPlayerID']])
        except KeyError:
            # This occurs if we have a bad pass, throws this data point away
            return
        dm.m[res] += 1

    def umat_incr(self, um, rrow):
        try:
            res = ( self.name_to_idx[ rrow['OriginPlayerID'] ],
                    self.name_to_idx[ rrow['DestinationPlayerID']])
            um.m[res] += 1
            res = (self.name_to_idx[rrow['DestinationPlayerID']],
                   self.name_to_idx[rrow['OriginPlayerID']])
            um.m[res] += 1
        except KeyError:
            # This occurs if we have a bad pass, throws this data point away
            return

### END ConnectivityMatrixFactory ######################################
########################################################################

def CMFGET(pathglob):
    CMF = ConnectivityMatrixFactory('data/huskiespassingevents.csv')
    mats = CMF.get_all_mats(pathglob)
    print(mats)
    return mats

if __name__ == '__main__':
    if len(sys.argv) != 2:
        infiles = 'data/huskiespassingevents.csv'
    else:
        infiles = sys.argv[1]
    mats = CMFGET(infiles)
    print(mats[0]['umat'].calc_eigs())
    # heatmap(M.diadjmat)
    # heatmap(M.uadjmat)

