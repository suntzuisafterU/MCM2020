'''A script whose job it is to read in plays and graph them on a 3d axis (space and time).'''
import sys as sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def readPlay(filename, isRand=False, gameNum=0, endShot=False):
    '''
        Three inputs. Do we want random plays, Which game in particular 0 is any of them and did the play
        lead to a shot. We will then read in plays that satisfy these constraints
    :param isRand: Do we want random plays.
    :param gameNum: Which game in particular 0 is any of them
    :param isShot: display games that lead to a shot.
    :return: Nothing but it will display a graph
    '''
    first = True
    offset = 0

    xAxis = []
    yAxis = []
    zAxis = []

    f = open(filename, "r")
    next(f)

    for line in f:
        linesplt = line.rstrip("\n").split(",")


        print(linesplt[8])

        #Normalizing the time.
        if first:
            first = False
            offset = float(linesplt[5])

        xAxis.append(float(linesplt[8]))
        yAxis.append(float(linesplt[9]))
        zAxis.append(float(linesplt[5]) - offset)
    f.close()

    print(xAxis, yAxis, zAxis)

    if(isShot):
        if(linesplt[6].__eq__("Shot")):
            playPlot3d.plot(xAxis, yAxis, zAxis)
    else:
        playPlot3d.plot(xAxis, yAxis, zAxis)


if __name__ == '__main__':
    print(sys.argv)
    playPlot = plt.figure()
    playPlot3d = playPlot.gca(projection='3d')

    playPlot3d.set_xlabel('X Axis')
    playPlot3d.set_ylabel('Y Axis')
    playPlot3d.set_zlabel('Time')

    for i in range(200):
        try:
            readPlay("data/plays/HPlays/Hplay"+(str(i).zfill(4)), endShot=True)
        except:
            print("Bad Data###############")
    plt.show()