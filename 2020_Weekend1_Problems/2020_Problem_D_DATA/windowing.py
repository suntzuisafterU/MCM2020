from value import *
from readplay import *
import numpy as np

def windower(window_size, analysisfn, myplay):

    xs = []
    ys = []
    for i in range(len(myplay) - window_size):
        myslice = myplay[i:i+window_size]
        ys.append(analysisfn(myslice))    
        xs.append(time_average(myslice))

    return xs, ys


def windower3d(window_size, analysisfn, myplay):


    xs = []
    ys = []
    zs = []
    for i in range(len(myplay) - window_size):
        myslice = myplay[i:i+window_size]
        zs.append(analysisfn(myslice))
        ys.append(averageY(myslice))
        xs.append(averageX(myslice))

    return xs, ys, zs


def time_average(slicein):

    time = 0
    for i in slicein:
        time += i[5]
    return time / len(slicein)


def averageX(slicein):
    xpos = 0
    for i in slicein:
        xpos += i[8]
    return xpos / (len(slicein) + 1)


def averageY(slicein):
    ypos = 0
    for i in slicein:
        ypos += i[9]
    return ypos / (len(slicein) + 1)


def smoothing(pts, dist):
    newpts = []
    for i in range(len(pts) - len(dist)):
        newpt = 0
        for j in range(len(dist)):
            newpt += pts[i + j] * dist[j]
        newpts.append(newpt)

    return newpts


def gaussian(mu, sig, size):
    x = np.linspace(-3, 3, 5)
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))






