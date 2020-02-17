
from value import *
from connectivity_matrix import *
from groundtruth import *
from readplay import *
import csv

metrics = [ground_truth, ground_truth_offense, ground_truth_defense,
           shotsAllowedVal, shotsTakenVal, flowEV, tempoEV,
           # breadthEV,
           network_strength_eigen_value, algebraic_connectivity,
           # normalized_algebraic_connectivity,
           triad_sum, diadic_sum
           ]

def anal_game_off_metrics():
    f = open(f"data/groundtruths/game_{team}_offensive_groundtruths.csv", "r")

    data = []
    for line in f:
        data.append(line.rstrip().rsplit(","))
    del data[0] # delete data header

    metricdata = []
    header = ["GameName", "GroundTruth"]
    for metric in metrics:
        name = str(metric.__name__)
        if name == 'wrapper':
            raise AssertionError # Should have a different name
        else:
            header.append(name)

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


    with open(f"data/groundtruths/game_{team}_metricdata.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(metricdata)



def plays_all_data():
    data = []
    metric_data = []
    header = []
    for metric in metrics:
        header.append(str(metric.__name__))

    plays = read_glob_of_plays("data/plays/play*")

    for p in plays:
        res = [metric(p) for metric in metrics]
        metric_data.append(res)

    final = pd.DataFrame(data=metric_data, columns=header)

    print(final)

    with open(f"data/groundtruths/allplays_{team}_metricdata.csv", "w") as f:
        final.to_csv(f)


def game_all_data():
    df = pd.read_csv("data/matches.csv")
    header = []
    # there are 38 games
    # metric_data = {i: np.zeros((len(metrics),1), np.float) for i in range(1,39)}
    metric_data = []
    for metric in metrics:
        name = str(metric.__name__)
        if name == 'wrapper':
            raise AssertionError # Should have a different name
        else:
            header.append(name)

    games = read_glob_of_plays("data/games/game*")

    for g in games:
        temp_event = g[0]
        res = [metric(g) for metric in metrics]
        metric_data.append(res)
        # metric_data[temp_event["MatchID"]] += res

    metric_data.append(np.zeros((len(metrics),), np.float)) # dirty hack, add row of zeroes
    metric_data = np.array(metric_data)

    s1 = metric_data[1::2]
    s2 = metric_data[::2]

    s3 = s1 + s2

    mdf = pd.DataFrame(s3, columns=header)
    final = pd.concat([df, mdf], axis=1)
    print(final)

    with open(f"data/groundtruths/fullgame_{team}_metricdata.csv", "w") as f:
        final.to_csv(f)

game_all_data()
plays_all_data()
anal_game_off_metrics()

