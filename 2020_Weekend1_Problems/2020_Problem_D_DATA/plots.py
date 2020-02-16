import matplotlib.pyplot as plt
from matplotlib import cm
from windowing import *
from value import *

def plot2dscatter(playlist, funclist):

    for play in playlist:
        for i in range(1, 10):
            for func in funclist:
                xs, ys = windower(i, func, play)
                plt.scatter(xs, ys, color=(float("0."+str(i)), .5, .5))
    plt.show()


#pathglob = input("pathglob?")
plays = lists_and_spectral_dicts("data/plays/game0002")


funcs = [ballX, ballY]

plot2dscatter(plays, funcs)


#
# #ax = mysurf.add_subplot(111, projection='3d')
# ax = mysurf.gca(projection='3d')
# xss,yss,zss = [], [], []
#
# for playlists, playdicts in plays:
#     for i in range(1, 12):
#         xs, ys, zs = windower3d(i, flowEV, playlist)
#         xss += xs
#         yss += ys
#         zss += zs
#
# xss = smoothing(xss, smoothingdist)
# yss = smoothing(yss, smoothingdist)
# zss = smoothing(zss, smoothingdist)
#
# ax.scatter(xss, yss, zss, cmap=cm.coolwarm)
# plt.show()
#
#
# "
# mysurf = plt.figure()
#

