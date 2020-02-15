from value import *
import numpy as np
import matplotlib.pyplot as mp
from mpl_toolkits.mplot3d import Axes3D
def windower(window_size, analysisfn, play, schema):

    myplay = readplay(play, schema)

    xs = []
    ys = []
    for i in range(len(myplay) - window_size):
        myslice = myplay[i:i+window_size]
        ys.append(analysisfn(myslice))    
        xs.append(time_average(myslice))

    return xs, ys

def time_average(slicein):
    time = 0
    for i in slicein:
        time += i[5]
    return time / len(slicein)

def _3dgen(analysisfn, play, schema):

    myplay = readplay(play, schema)
    xs = []
    ys = []
    ts = []

    for play in myplay:
        xs.append(play[9])
        ys.append(play[10])
        ts.append(play[5])


    return np.array(xs), np.array(ys), np.array(ts)
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
for j in range(1, 100):
    for i in range(1, 10):
        xs, ys = windower(i, flowEV, j, "Hplay")
        mp.scatter(xs, ys, color=(float("0."+str(i)), .5, .5))
        xt, yt = windower(i, tempoEV, j, "Hplay")
        mp.scatter(xt, yt, color=(.5, float("0."+str(i)), .5))
        xx, yx = windower(i, ballX, j, "Hplay")
        mp.scatter(xx, yx, color=(.5, .5, float("0."+str(i))))
    mp.show()

