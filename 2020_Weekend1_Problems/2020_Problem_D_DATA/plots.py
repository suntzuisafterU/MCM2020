import matplotlib.pyplot as plt
from matplotlib import cm
from windowing import *
from value import *
from random import random
from mpl_toolkits.mplot3d import Axes3D


def plot2d(playlist, funclist, plottype, smoother=None):

    g, b = random(), random()
    for play in playlist:
        for i in range(1, 10):
            for func in funclist:
                xs, ys = windower(i, func, play)
                if smoother is not None:
                    xs = smoothing(xs, smoother)
                    ys = smoothing(ys, smoother)
                plottype(xs, ys, color=(float("0."+str(i)), g, b))
    plt.show()


def plot3d(playlist, funclist, smoother=None):

    mysurf = plt.figure()
    ax = mysurf.add_subplot(111, projection='3d')

    for play in playlist:
        for i in range(1, 99):
            for func in funclist:
                xs, ys, zs = windower3d(i, func, play)
                if smoother is not None:
                    xs = smoothing(xs, smoother)
                    ys = smoothing(ys, smoother)
                    zs = smoothing(zs, smoother)

    ax.scatter(xs, ys, zs, cmap=cm.coolwarm)
    plt.show()



if __name__ == "__main__":

    plays = read_glob_of_plays("data/plays/game0002")
    mysmoother = gaussian(3, 3, 100)
    funcs = [flowEV]

    #plot2d(plays, funcs, plt.scatter)
    plot3d(plays, funcs)
