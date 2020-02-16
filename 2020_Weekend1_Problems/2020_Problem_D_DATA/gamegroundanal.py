
from value import *
from connectivity_matrix import *
from readplay import readplay

metrics = [clearVal, shotsAllowedVal, shotsEV, flowEV, tempoEV,
           breadthEV, evan_call_this_for_eigs, algebraic_connectivity,
           normalized_algebraic_connectivity, triad_sum, diadic_sum]

def anal_game_off_metrics():
    f = open("data/groundtruths/gameoffensivegroundtruths.csv", "r")

    data = []
    for line in f:
        data.append(line.rstrip().rsplit(","))


    metricdata = []
    header = ["GameName", "GroundVal"]
    for metric in metrics:
        header.append(str(metric.__name__))

    metricdata.append(header)

    for half in data:
        thishalf = []
        halfname = half[0]
        halfgroundval = float(half[1])
        thishalf.append(halfname)
        thishalf.append(halfgroundval)
        thisplay = readplay("data/games/" + halfname)
        for metric in metrics:
            metricval = metric(thisplay)
            thishalf.append(metricval)

        metricdata.append(thishalf)


    f = open("data/groundtruths/metricdata.csv", "w")

    for line in metricdata:
        for item in line:
            f.write(str(item))
            f.write(",")
        f.write("\n")

    print(metricdata)



def anal_play_off_metrics():
    f = open("data/groundtruths/play_offenseive_groundtruths.csv", "r")

    data = []
    for line in f:
        data.append(line.rstrip().rsplit(","))


    metricdata = []
    header = ["GameName", "GroundVal"]
    for metric in metrics:
        header.append(str(metric.__name__))

    metricdata.append(header)

    for half in data:
        thishalf = []
        halfname = half[0]
        halfgroundval = float(half[1])
        thishalf.append(halfname)
        thishalf.append(halfgroundval)
        print(halfname)
        thisplay = readplay("data/plays/" + halfname)
        for metric in metrics:
            metricval = metric(thisplay)
            thishalf.append(metricval)

        metricdata.append(thishalf)


    f = open("data/groundtruths/playmetricdata.csv", "w")

    for line in metricdata:
        for item in line:
            f.write(str(item))
            f.write(",")
        f.write("\n")

    print(metricdata)



anal_play_off_metrics()