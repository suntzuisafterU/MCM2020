from readplay import readplay

def normtime(play):

    data = readplay(play)

    myoffset = data[0][5]

    for i in data:
        i[5] -= myoffset


    return data


def playlen(play):

    data = readplay(play)

    return abs(data[0][5] - data[-1][5])


def avgplaylen():

    t = 0

    for i in range(1, 1682):
        t += playlen(i)
    
    return t / 1682   


