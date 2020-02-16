from value import *
from readplay import *
from random import randint
from connectivity_matrix import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import sys

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


"""
xs, ys, ts = _3dgen(flowEV, 30, "Hplay")
fig = mp.figure()
ax = fig.gca(projection='3d')
ax.plot_trisurf(xs, ys, ts, linewidth=0.2, antialiased=True)
fig.show()
"""
"""
for i in range(1, 100):
    xf, yf = windower(50, flowEV, i, "game")
    xs, ys = windower(50, shotsEV, i, "game")
    xt, yt = windower(50, tempoEV, i, "game")
    xb, yb = windower(50, breadthEV, i, "game")
    xx, yx = windower(50, ballX, i, "game")
    xy, yy = windower(50, ballY, i, "game")
    mp.scatter(xs, ys)
    mp.scatter(xb, yb)
    mp.scatter(xt, yt)
    mp.scatter(xf, yf)
    mp.scatter(xx, yx)
    mp.scatter(xy, yy)
    mp.show()
"""

def smoothing(pts, dist):
    newpts = []
    for i in range(len(pts) - len(dist)):
        newpt = 0
        for j in range(len(dist)):
            newpt += pts[i + j] * dist[j]
        newpts.append(newpt)

    return newpts



# for play in plays:
#     for i in range(1, 10):
#         xs, ys = windower(i, flowEV, play)
#         mp.scatter(xs, ys, color=(float("0."+str(i)), .5, .5))
#         xt, yt = windower(i, tempoEV, play)
#         mp.scatter(xt, yt, color=(.5, float("0."+str(i)), .5))
#         xx, yx = windower(i, ballX, play)
#         mp.scatter(xx, yx, color=(.5, .5, float("0."+str(i))))
#     mp.show()
mysurf = plt.figure()


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

x_values = np.linspace(-3, 3, 5)

mu = 2
sig = 3
smoothingdist = gaussian(x_values, mu, sig)
#
# plt.plot(x_values, smoothingdist)
# plt.show()




# pathglob = input("pathglob?")
pathglob = "data/plays/play000?H"

plays = lists_and_spectral_dicts(pathglob)

#ax = mysurf.add_subplot(111, projection='3d')
ax = mysurf.gca(projection='3d')
xss,yss,zss = [], [], []

for playlist, playdicts in plays:
    for i in range(1, 12):
        xs, ys, zs = windower3d(i, evan_call_this_for_eigs, playdicts)
        xss += xs
        yss += ys
        zss += zs

xss = smoothing(xss, smoothingdist)
yss = smoothing(yss, smoothingdist)
zss = smoothing(zss, smoothingdist)

ax.scatter(xss, yss, zss, cmap=cm.coolwarm)
plt.show()


