'''A script whose job it is to read in plays and graph them on a 3d axis (space and time).'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def readPlay(filename, isRand=False, gameNum=0, isShot=False):
    '''
        Three inputs. Do we want random plays, Which game in particular 0 is any of them and did the play
        lead to a shot. We will then read in plays that satisfy these constraints
    :param isRand: Do we want random plays.
    :param gameNum: Which game in particular 0 is any of them
    :param isShot: display games that lead to a shot.
    :return: Nothing but it will display a graph
    '''

    playPlot = plt.figure()
    playPlot3d = playPlot.gca(projection='3d')

    xAxis = []
    yAxis = []
    zAxis = []

    f = open(filename, "r")
    for line in f:
        linesplt = line.rstrip("\n").split(",")

        if(not linesplt[0].isdigit()):
            continue

        xAxis.append(float(linesplt[8]))
        yAxis.append(float(linesplt[9]))
        zAxis.append(float(linesplt[5]))
    f.close()

    print(xAxis, yAxis, zAxis)
    playPlot3d.plot(xAxis, yAxis, zAxis)
    playPlot3d.set_xlabel('X Axis')
    playPlot3d.set_ylabel('Y Axis')
    playPlot3d.set_zlabel('Time')

    plt.show()

if __name__ == '__main__':
    readPlay("data/plays/play0")