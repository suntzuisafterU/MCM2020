'''A script whose job it is to read in plays and graph them on a 3d axis (space and time).'''
import sys as sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as m
import readplay as rp


def pltPlay(filename, isRand=False, gameNum=0, endShot=False):
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

        #Normalizing the time.
        if first:
            first = False
            offset = float(linesplt[5])

        xAxis.append(float(linesplt[8]))
        yAxis.append(float(linesplt[9]))
        zAxis.append(float(linesplt[5]) - offset)
    f.close()

    if(endShot):
        if(linesplt[6].__eq__("Shot")):
            playPlot3d.plot(xAxis, yAxis, zAxis)
    else:
        playPlot3d.plot(xAxis, yAxis, zAxis)


def toPolar(x, y):
    return m.sqrt(x**2 + (y-50)**2), m.atan2(y, x)

def groundLost(play):
    startTime = play[0]["EventTime"]
    endTime = play[-1]["EventTime"]
    groundGained = 0

    for i in play:
        if i["TeamID"] != "Huskies":
            rSrc, thetaSrc = toPolar(float(i["EventOrigin_x"]), float(i["EventOrigin_y"]))
            rDst, thetaDst = toPolar(float(i["EventDestination_x"]), float(i["EventDestination_y"]))
            groundGained += rDst - rSrc

    if (endTime - startTime) == 0:
        return -groundGained
    else:
        return  -(groundGained*(1 / (endTime - startTime)))

def shotsAllowedVal(play):
    totVal = 0

    for i in play:
        if i["TeamID"] != "Huskies" and i["EventSubType"] == "Shot":
            rSrc, thetaSrc = toPolar(float(i["EventOrigin_x"]), float(i["EventOrigin_y"]))

            if(rSrc > 35):
                totVal += rSrc - (rSrc/thetaSrc)
            else:
                totVal += rSrc * thetaSrc

    return totVal

#def defensiveMacho(play):
   # for i in play:
    #    if i["EventType"] == "Defensive"

def clearVal(play):
    totVal = 0

    for i in play:
        if i["TeamID"] == "Huskies":
            if i["EventSubType"] == "Clearance":
                r, theta = toPolar(i["EventDestination_x"], i["EventDestination_y"])
                if r < 20:
                    totVal += (r * theta) - 80
                elif r*theta < 35:
                    totVal += (r * theta) - 30
                else:
                    totVal += r
    return totVal




if (__name__ == '__main__'):
    playPlot = plt.figure()
    playPlot3d = playPlot.gca(projection='3d')

    playPlot3d.set_xlabel('X Axis')
    playPlot3d.set_ylabel('Y Axis')
    playPlot3d.set_zlabel('Time')

    try:
        print("Ground:  ", groundLost(rp.readplay("data/plays/game/game0001")))
        print("Clearance:  ", clearVal(rp.readplay("data/plays/game/game0001")))
        print("Shots:  ",  shotsAllowedVal(rp.readplay("data/plays/game/game0001")))

        pltPlay("data/plays/OPlays/Oplay0004")

        print("Ground:  ", groundLost(rp.readplay("data/plays/game/game0002")))
        print("Clearance:  ", clearVal(rp.readplay("data/plays/game/game0002")))
        print("Shots:  ", shotsAllowedVal(rp.readplay("data/plays/game/game0002")))
        pltPlay("data/plays/OPlays/Oplay0005")


        print("Ground ", groundLost(rp.readplay("data/plays/game/game0003")))
        print("Clearance:  ", clearVal(rp.readplay("data/plays/game/game0003")))
        print("Shots:  ",shotsAllowedVal(rp.readplay("data/plays/game/game0003")))
        pltPlay("data/plays/OPlays/Oplay0006")

        #plt.show()

    except:
        pass

    #plt.show()
    #for i in rp.read_glob_of_plays("data/plays/OPlays/*"):
        #print(groundLost(i))

