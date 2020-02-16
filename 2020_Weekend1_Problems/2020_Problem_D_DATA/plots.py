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
            g, b = random(), random()
            for i in range(30,31):  # this parameter is EXTREMELY sensitive actually a window
                                    # size of ~30 gives a strong relation to alg-con
                xs, ys = windower(i, func, play)
                if smoother is not None:
                    xs = smoothing(xs, smoother)
                    ys = smoothing(ys, smoother)
                plottype(xs, ys, label=str(func), color=(float("0."+str(i)), g, b))

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
    mysmoother = gaussian(3, 3, 50)

    gameglob = input("what glob friend? ")
    plays = read_glob_of_plays("data/plays/" + gameglob)


    funcs = [algebraic_connectivity]

    plot2d(plays, funcs, plt.plot, mysmoother)

    funcs = [flowEV]

    plot2d(plays, funcs, plt.plot, mysmoother)

    funcs = [algebraic_connectivity, flowEV, shotsEV]

    plot2d(plays, funcs, plt.plot, mysmoother)
    #
    # funcs = [flowEV]
    # plot3d(plays, funcs, mysmoother)
