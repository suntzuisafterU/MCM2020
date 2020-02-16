

terminals = ["Free Kick", "Foul", "Offside", "Substitution", "Interruption"]

f = open("data/fullevents.csv", "r")

event_list = []
for line in f:
    event_list.append(line.split(","))


header = event_list.pop(0)
header = ",".join(header)

def playParser(ev_list, init_max):
    prefix = "data/plays/"
    plays = []
    curr_game = ev_list[0][0]
    current_initiative = ev_list[0][1]
    initiative_stack = 1

    current_play = []

    opstackval = 1
    for play in ev_list:

        if play[1] == current_initiative and initiative_stack < init_max:
            initiative_stack += 1
            if opstackval > 1:
                opstackval = opstackval * 0.9  # this is really shitty exponential averaging

        elif play[1] != current_initiative:
            initiative_stack -= opstackval
            opstackval *= 1.3
        
        if initiative_stack < 1 or play[0] != curr_game or play[6] in terminals:  # we have a new initiative starting
            if len(current_play) > 5:
                plays.append(current_play)
            current_play = []
            initiative = 1
            current_initiative = play[1]
            curr_game = play[0]
            opstackval = 1

        current_play.append(play)

    playnum = 0
    for play in plays:
        playboys = play[0][1][0]
        fname = f"{prefix}play{playnum:04d}{playboys}"
        f = open(fname, "w")
        f.write(header)
        for ev in play:
            for el in ev:
                f.write(el)
                if not "\n" in el:
                    f.write(",")
        f.close()
        playnum += 1
    return plays


def gameParser(ev_list):
    prefix = "data/games/"

    games = []
    current_game = []

    gamenum = ev_list[0][0]
    for i in range(len(ev_list) - 1):
        #if ev_list[i + 1][0] == gamenum: 
        #if "Opp" not in ev_list[i][1]:
        current_game.append(ev_list[i])
        #else:
        #    games.append(current_game)
        #    gamenum = ev_list[i + 1][0]
        #    current_game = []
        if float(ev_list[i + 1][5]) < float(ev_list[i][5]):
            # print(float(ev_list[i+1][5]), float(ev_list[i][5]), ev_list[i][0])
            games.append(current_game)
            gamenum = ev_list[i + 1][0]
            current_game = []
    gamenum = 1
    for game in games:
        f = open(f"{prefix}game{int(game[1][0]):02d}_{game[1][4]}", "w")
        f.write(header)
        for ev in game:
            for el in ev:
                f.write(el)
                if not "\n" in el:
                    f.write(",")
        f.close()
        gamenum += 1


gameParser(event_list)
playParser(event_list, 4)
        
    




