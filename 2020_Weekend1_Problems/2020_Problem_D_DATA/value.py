from timing import *
from scipy.stats import linregress
import glob
import math

class EV:

    def __init__(self, play):
        self.BEV = breadthEV(play)
        self.TEV = tempoEV(play)
        self.FEV = flowEV(play)
        self.SEV = shotsEV(play)
        self.totalEV = sum([self.BEV, self.TEV, self.FEV, self.SEV])

    def report(self):

        print("Breadth EV for this play was", self.BEV)
        print("Tempo EV for this play was",   self.TEV)
        print("Flow EV for this play was",    self.FEV)
        print("Shots EV for this play was",   self.SEV)
        print("Total EV for this play was",   self.totalEV)


def breadthEV(play):
    playerset = set()
    for i in play:
        if i["TeamID"] == "Huskies":
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
        if play[i]["TeamID"] == "Huskies" and play[i+1]["TeamID"] == "Huskies":
            passtime += (play[i+1]["EventTime"] - play[i]["EventTime"])
            totalpass += 1
    if totalpass != 0:
        return passtime / totalpass
    else:
        return 0    


def flowEV(play):
    flowmetric = 1

    for i in play:
        if i["TeamID"] == "Huskies":
            flowmetric *= 1.2
        else:
            flowmetric *= 0.8

    return flowmetric


def shotsEV(play):
    shots = 0
    for i in play:
        if i["EventType"] == "Shot" and i["TeamID"] == "Huskies":
            shots += 10
        elif i["EventType"] == "Shot":
            shots -= 10
    return shots



