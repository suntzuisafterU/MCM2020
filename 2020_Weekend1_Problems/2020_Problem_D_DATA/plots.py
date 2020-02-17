import matplotlib.pyplot as plt
from matplotlib import cm
from windowing import *
from value import *
from random import random
from mpl_toolkits.mplot3d import Axes3D
from connectivity_matrix import *


def plot2d(playlist, funclist, plottype, smoother=None):


    for play in playlist:

        for func in funclist:

            for i in range(30,31):  # this parameter is EXTREMELY sensitive actually a window
                                    # size of ~30 gives a strong relation to alg-con
                xs, ys = windower(i, func, play)
                if smoother is not None:
                    xs = smoothing(xs, smoother)
                    ys = smoothing(ys, smoother)
                plottype(xs, ys, label=str(func.__name__))
    plt.legend()
    plt.show()


def plot3d(playlist, funclist, smoother=None):

    mysurf = plt.figure()
    ax = mysurf.add_subplot(111, projection='3d')
    xss, yss, zss = [], [], []
    for play in playlist:
        for i in range(30,40):
            for func in funclist:
                xs, ys, zs = windower3d(i, func, play)

                xss += xs
                yss += ys
                zss += zs

    if smoother is not None:
        xss = smoothing(xss, smoother)
        yss = smoothing(yss, smoother)
        zss = smoothing(zss, smoother)
    ax.scatter(xss, yss, zss, cmap=cm.coolwarm)
    plt.show()



if __name__ == "__main__":


    mysmoother = gaussian(3, 3, 15)

    gameglob = input("what glob friend? ")



    plays_first = read_glob_of_plays(gameglob)

    # plays_first =  read_glob_of_plays("data/games/game" + f"{gameglob:02}" + "_1H")
    # plays_second = read_glob_of_plays("data/games/game" + f"{gameglob:02}" + "_2H")


    funcs = [algebraic_connectivity, tempoEV]
    plot2d(plays_first, funcs, plt.plot)
   # plot2d(plays_second, funcs, plt.plot, mysmoother)

