from readplay import readplay
from timing import *
from scipy.stats import linregress
from os import listdir
class Play:
    
    def __init__(self, bEV, tEV, fEV, sEV, playnum):
        self.bEV = bEV
        self.tEV = tEV
        self.fEV = fEV
        self.sEV = sEV
        self.TEV = sum([bEV, tEV, fEV, sEV])
        self.playnum = playnum

    def query(self):
        
        print()
        print("For Play Number", self.playnum)
        print("Breadth EV was:", self.bEV)    
        print("Tempo EV was:",   self.tEV)    
        print("Flow EV was:",    self.fEV)    
        print("Shots EV was:",   self.sEV)    
        print("Total EV was",    self.TEV)
        
        

def EV(play, schema):

    
    myplay = readplay(play, schema)
            
    bEV = breadthEV(myplay)
    tEV = tempoEV(myplay, play)
    fEV = flowEV(myplay)
    sEV = shotsEV(myplay)

    return Play(bEV, tEV, fEV, sEV, play)


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
    schema = input("What types of files to provide analysis for?")

    thisdir = listdir(".")
    totalH = sum([1 for i in thisdir if schema in i])

    playlist = []
    for i in range(1,totalH):
        playlist.append(EV(i, schema)) 

    playlist.sort(key=lambda x: x.sEV)

    shots = [i.sEV for i in playlist]
    tempo = [i.tEV for i in playlist]
    breadth = [i.bEV for i in playlist]
    flow = [i.fEV for i in playlist]

    #for i in playlist:
    #    i.query()

    print(linregress(breadth, tempo))
