
def normtime(play):
    data = play
    myoffset = data[0]["EventTime"]
    for i in data:
        i[5] -= myoffset
    return data


def playlen(play):
    return abs(play[0]["EventTime"] - play[-1]["EventTime"])



