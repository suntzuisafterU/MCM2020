import sys

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import connectivity_matrix as cn


def eigs_eq(m1: cn.Adjmat, m2: cn.Adjmat):
    eig1 = list(m1.calc_eigs())
    eig2 = list(m2.calc_eigs())
    temp = eig2.copy()
    for t in eig1:
        if t in temp:
            temp.remove(t)
        else:
            return False
    if len(temp) != 0:
        return False
    print("============================")
    # print(m1.name, m1.m, eig1)
    # print(m2.name, m2.m, eig2)
    print(m1.name, m2.name)
    # plt.imshow(m1.m)
    # plt.show()
    # plt.imshow(m2.m)
    # plt.show()

    return True

def get_all_eigs(ms):
    res = []
    for m in ms:
        res.append(m.calc_eigs())
    return res


if __name__ == "__main__":
    assert len(sys.argv) > 1
    ins = sys.argv[1] # glob
    print(ins)
    ms = cn.CMFGET(ins)
    ms = [m['umat'] for m in ms]
    # eig values
    eigpairs = [[eigs_eq(m1, m2) if m1.name is not m2.name else None for m1 in ms] for m2 in ms]
    print('here')








