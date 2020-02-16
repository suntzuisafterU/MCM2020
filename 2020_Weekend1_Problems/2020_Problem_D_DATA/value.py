from timing import *
from scipy.stats import linregress
import glob
import math

def breadthEV(play):
    playerset = set()
    for i in play:
        if i[1] == "Huskies":
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


def shotsDistEV(play):
    shots = 0

    for i in play:
        if i["EventType"] == "Shot" and i["TeamID"] == "Huskies":
            x = (i["EventOrigin_x"] - 50) ** 2
            y = (i["EventOrigin_y"] - 50) ** 2
            dist = abs(math.sqrt(x + y))
            shots += 1 * dist
        elif i["EventType"] == "Shot":
            x = (i["EventOrigin_x"] - 50) ** 2
            y = (i["EventOrigin_y"] - 50) ** 2
            dist = abs(math.sqrt(x + y))
            shots -= 1 * dist
    return shots

