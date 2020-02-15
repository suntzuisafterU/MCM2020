from readplay import readplay
from timing import *

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
        
        

def EV(play):


    myplay = readplay(play)
            
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




def tempoEV(play, playnum):

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
            flowmetric *= 1.1
        else:
            flowmetric *= 0.9

    return flowmetric


def shotsEV(play):

    shots = 0
    for i in play:
        if i[7] == "Shot":
            shots += 10

    return shots


playlist = []
for i in range(1,1600):
    playlist.append(EV(i)) 

playlist.sort(key=lambda x: x.tEV)

for i in playlist:
    i.query()
