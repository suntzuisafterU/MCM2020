from readplay import readplay
from timing import *
from scipy.stats import linregress
from os import listdir
import glob


class Play:
    
    def __init__(self, bEV, tEV, fEV, sEV, play):
        self.bEV = bEV
        self.tEV = tEV
        self.fEV = fEV
        self.sEV = sEV
        self.TEV = sum([bEV, tEV, fEV, sEV])
        # TODO: Extract actual play number here
        self.playfile = play

    def query(self):
        
        print()
        print("For Play Number", self.playfile)
        print("Breadth EV was:", self.bEV)    
        print("Tempo EV was:",   self.tEV)    
        print("Flow EV was:",    self.fEV)    
        print("Shots EV was:",   self.sEV)    
        print("Total EV was",    self.TEV)
        
        

def EV(path):

    myplay = readplay(path)
            
    bEV = breadthEV(myplay)
    tEV = tempoEV(myplay)
    fEV = flowEV(myplay)
    sEV = shotsEV(myplay)

    return Play(bEV, tEV, fEV, sEV, path)


def breadthEV(play):

    playerset = set()
    for i in play:
        if i[1] == "Huskies":
            playerset = playerset | set(i[2])

    return len(playerset) 


def ballX(play):
    xpos = 0
    for i in play:
        xpos += i[9]
    xpos = xpos / len(play)
    return xpos


def ballY(play):
    ypos = 0
    for i in play:
        ypos += i[10]
    ypos = ypos / len(play)
    return ypos

def tempoEV(play):

    passtime = 0
    totalpass = 0
    for i in range(len(play) - 1):
        if play[i][1] == "Huskies" and play[i+1][1] == "Huskies":
            passtime += (play[i+1][5] - play[i][5])
            totalpass += 1


    if totalpass != 0:
        return passtime / totalpass
    else:
        return 0    


def flowEV(play):

    flowmetric = 1

    for i in play:
        if i [1] == "Huskies":
            flowmetric += 1.01
        else:
            flowmetric -= 0.99

    return flowmetric


def shotsEV(play):

    shots = 0
    for i in play:
        if i[7] == "Shot" and i[1] == "Huskies":
            shots += 10
        elif i[7] == "Shot":
            shots -= 10

    return shots

if __name__ == "__main__":
    schema = input("Path glob for files? ")

    playlist = glob.glob(schema)

    res = []
    for play in playlist:
        res.append(EV(play))

    res.sort(key=lambda x: x.sEV)

    shots = [i.sEV for i in res]
    tempo = [i.tEV for i in res]
    breadth = [i.bEV for i in res]
    flow = [i.fEV for i in res]

    #for i in playlist:
    #    i.query()

    print(linregress(breadth, tempo))
