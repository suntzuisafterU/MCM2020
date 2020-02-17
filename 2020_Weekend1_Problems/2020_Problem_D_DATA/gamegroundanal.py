
from value import *
from connectivity_matrix import *
from readplay import readplay

metrics = [clearVal, shotsAllowedVal, shotsEV, flowEV, tempoEV,
           breadthEV, evan_call_this_for_eigs, algebraic_connectivity,
           normalized_algebraic_connectivity, triad_sum, diadic_sum]

def anal_game_off_metrics():
    f = open(f"data/groundtruths/game_{team}_offensive_groundtruths.csv", "r")

    data = []
    for line in f:
        data.append(line.rstrip().rsplit(","))
    del data[0] # delete data header


    metricdata = []
    header = ["GameName", "GroundTruth"]
    for metric in metrics:
        header.append(str(metric.__name__))

    metricdata.append(header)

    for half in data:
        thishalf = []
        halfname = half[0]
        halfgroundval = float(half[2])
        thishalf.append(halfname)
        thishalf.append(halfgroundval)
        thisplay = readplay("data/games/" + halfname)
        for metric in metrics:
            metricval = metric(thisplay)
            thishalf.append(metricval)

        metricdata.append(thishalf)


    f = open(f"data/groundtruths/game_{team}_metricdata.csv", "w")

    for line in metricdata:
        for item in line:
            f.write(str(item))
            f.write(",")
        f.write("\n")

    f.close()



def anal_play_off_metrics():
    f = open(f"data/groundtruths/play_{team}_offensive_groundtruths.csv", "r")

    data = []
    for line in f:
        data.append(line.rstrip().rsplit(","))
    del data[0] # delete header


    metricdata = []
    header = ["GameName", "GroundTruth"]
    for metric in metrics:
        header.append(str(metric.__name__))

    metricdata.append(header)

    for half in data:
        thishalf = []
        halfname = half[0]
        halfgroundval = float(half[2])
        thishalf.append(halfname)
        thishalf.append(halfgroundval)
        thisplay = readplay("data/plays/" + halfname)
        for metric in metrics:
            metricval = metric(thisplay)
            thishalf.append(metricval)

        metricdata.append(thishalf)


    f = open(f"data/groundtruths/play_{team}_metricdata.csv", "w")

    for line in metricdata:
        for item in line:
            f.write(str(item))
            f.write(",")
        f.write("\n")





anal_play_off_metrics()
anal_game_off_metrics()
