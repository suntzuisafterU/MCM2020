import statistics

def localize(playname):

    f = open(playname, "r")

    data = []

    for line in f:
        data.append(line.split(",")[8:])
        data[-1][-1] = data[-1][-1].rstrip()
        data[-1] = [int(i[0:-2]) for i in data[-1]]
    

    xs = []
    ys = []
    total = 0

    for line in data:
        xs += [line[0]] + [line[2]]
        ys += [line[1]] + [line[3]]
        total += 1

    avgx = sum(xs) / total
    avgy = sum(ys) / total    

    print(statistics.stdev(xs))

    print(avgx, avgy)


playname = input("which play? ")
playname = "play" + playname 
localize(playname)
    


