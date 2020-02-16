from readplay import readplay

def normtime(play):

    data = play

    myoffset = data[0][5]

    for i in data:
        i[5] -= myoffset

    return data


def playlen(play):

    return abs(play[0][5] - play[-1][5])


def avgplaylen():

    t = 0

    for i in range(1, 1682):
        t += playlen(i)
    
    return t / 1682   


