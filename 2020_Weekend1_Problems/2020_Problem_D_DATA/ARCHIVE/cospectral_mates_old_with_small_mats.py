import sys

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import d


def eigs_eq(m1 : d.LocalOnlyConnectivityMats,
            m2: d.LocalOnlyConnectivityMats):
    eig1 = list(m1.ueigs)
    eig2 = list(m2.ueigs)
    temp = eig2.copy()
    for t in eig1:
        if t in temp:
            temp.remove(t)
        else:
            return False
    if len(temp) != 0:
        return False
    print("============================")
    print(m1.name, m1.uadjmat, eig1)
    print(m2.name, m2.uadjmat, eig2)
    # plt.imshow(m1.uadjmat)
    # plt.imshow(m2.uadjmat)

    return True

def get_all_eigs(ms):
    res = []
    for m in ms:
        res.append(m.ueigs)
    return res

if __name__ == "__main__":
    assert len(sys.argv) > 1
    ins = sys.argv[1] # glob
    ms = d.get_all_mats(ins)
    # eig values
    eigpairs = [[eigs_eq(m1, m2) if m1.name is not m2.name else None for m1 in ms] for m2 in ms]
    print(eigpairs)
    print('here')








