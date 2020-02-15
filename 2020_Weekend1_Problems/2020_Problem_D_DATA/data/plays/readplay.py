

def readplay(playnum, schema):
    

    f = open(schema + f"{playnum:04d}", "r")

    data = []

    for line in f:
        if line [0] == "M":
            continue
        data.append(line.split(","))
        data[-1][-1] = data[-1][-1].rstrip()
        data[-1][0] = int(data[-1][0])
        data[-1][5] = float(data[-1][5])
        if data[-1][6] != "Substitution" and data[-1][6] != "Foul":

            for i in range(8, 12):
                data[-1][i] = float(data[-1][i])    
        
        else:
            for i in range(8, 12):
                data[-1][i] = 0

    return data
