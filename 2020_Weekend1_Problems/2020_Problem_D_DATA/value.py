from timing import *
from scipy.stats import linregress
import glob
import math as m

from globals import *


class EV:

    def __init__(self, play):
        self.BEV = breadthEV(play)
        self.TEV = tempoEV(play)
        self.FEV = flowEV(play)
        self.SEV = shotsEV(play)
        self.CEV = clearVal(play)
        self.GLEV = groundLost(play)
        self.totalEV = sum([self.BEV, self.TEV, self.FEV, self.SEV, self.CEV, self.GLEV])

    def report(self):

        print("Breadth EV for this play was", self.BEV)
        print("Tempo EV for this play was",   self.TEV)
        print("Flow EV for this play was",    self.FEV)
        print("Shots EV for this play was",   self.SEV)
        print("Clear EV for this play was",   self.SEV)
        print("Ground Lost EV for this play was", self.SEV)
        print("Total EV for this play was",   self.totalEV)


def breadthEV(play):
    playerset = set()
    for i in play:
        if i["TeamID"] == team:
            playerset = playerset | set(i["OriginPlayerID"])
    return len(playerset)


def ballX(play):
    xpos = 0
    for i in play:
        xpos += i["EventOrigin_x"]
    xpos = xpos / len(play)
    return xpos


def ballY(play):
    ypos = 0
    for i in play:
        ypos += i["EventOrigin_y"]
    ypos = ypos / len(play)
    return ypos


def tempoEV(play):
    passtime = 0
    totalpass = 0
    for i in range(len(play) - 1):
        if play[i]["TeamID"] == team and play[i+1]["TeamID"] == team and play[i]["EventType"] == "Pass":
            passtime += (play[i+1]["EventTime"] - play[i]["EventTime"])
            totalpass += 1
    if totalpass != 0:
        return passtime / totalpass
    else:
        return 0    


def flowEV(play):
    flowmetric = 1

    for i in play:
        if i["TeamID"] == team:
            flowmetric *= 1.2
        else:
            flowmetric *= 0.8

    return flowmetric


def shotsEV(play):
    shots = 0
    for i in play:
        if i["EventType"] == "Shot" and i["TeamID"] == team:
            shots += 10
        elif i["EventType"] == "Shot":
            shots -= 10
    return shots

def lnDist(x1, y1, x2, y2, n):
    return (((x2-x1)**n + (y2 - y1)**n)**(1.0/14*n) - 2)

def sigmoid(x):
    return 1/(1 + m.exp(-x))

def shotsEV2(play):
    shots = 0
    for i in play:
        if i["EventType"] == "Shot" and i["TeamID"] == team:
            shots += 10 * sigmoid(lnDist(50, 50, float(i["EventOrigin_x"]), float(i["EventOrigin_y"]), 2))
        elif i["EventType"] == "Shot":
            shots -= 10 * sigmoid(lnDist(50, 50, float(i["EventOrigin_x"]), float(i["EventOrigin_y"]), 2))
    return shots




def toPolar(x, y):
    return m.sqrt(x**2 + (y-50)**2), m.atan2(y, x)


def groundLost(play):
    startTime = play[0]["EventTime"]
    endTime = play[-1]["EventTime"]
    groundGained = 0

    for i in play:
        if i["TeamID"] != team:
            rSrc, thetaSrc = toPolar(float(i["EventOrigin_x"]), float(i["EventOrigin_y"]))
            rDst, thetaDst = toPolar(float(i["EventDestination_x"]), float(i["EventDestination_y"]))
            groundGained += rDst - rSrc

    if (endTime - startTime) == 0:
        return -groundGained
    else:
        return  -(groundGained*(1 / (endTime - startTime)))

def oriented_src(event):
    origX, origY = float(event["EventOrigin_x"]), float(event["EventOrigin_y"])
    dstX, dstY = float(event["EventDestination_x"]), float(event["EventDestination_y"])
    return abs(origX - dstX), abs(origY - dstY)

def shotsAllowedVal(play):
    totVal = 0
    count = 0
    for i in play:
        if i["TeamID"] != team and i["EventSubType"] == "Shot":
            xSrc, ySrc = oriented_src(i)
            rSrc, thetaSrc = toPolar(float(i["EventOrigin_x"]), float(i["EventOrigin_y"]))
            #print(rSrc, thetaSrc, float(i["EventOrigin_x"]), float(i["EventOrigin_y"]))
            count += 1

            if(rSrc > 35):
                totVal += rSrc*(thetaSrc)
            else:
                totVal += rSrc - (rSrc/thetaSrc)
    #print(count)
    return totVal

def shotsTakenVal(play):
    totVal = 0
    count = 0
    for i in play:
        if i["TeamID"] == team and i["EventSubType"] == "Shot":
            xSrc, ySrc = oriented_src(i)
            rSrc, thetaSrc = toPolar(float(i["EventOrigin_x"]), float(i["EventOrigin_y"]))
            #print(rSrc, thetaSrc, float(i["EventOrigin_x"]), float(i["EventOrigin_y"]))
            count += 1

            if(rSrc > 35):
                totVal += rSrc*(thetaSrc)
            else:
                totVal += rSrc - (rSrc/thetaSrc)
    #print(count)
    return totVal


#def defensiveMacho(play):
   # for i in play:
    #    if i["EventType"] == "Defensive"


def clearVal(play):
    totVal = 0

    for i in play:
        if i["TeamID"] == team:
            if i["EventSubType"] == "Clearance":
                r, theta = toPolar(i["EventDestination_x"], i["EventDestination_y"])
                if r < 20:
                    totVal += (r * theta) - 80
                elif r*theta < 35:
                    totVal += (r * theta) - 30
                else:
                    totVal += r
    return totVal
