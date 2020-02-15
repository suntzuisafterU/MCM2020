

terminals = ["Free Kick", "Foul", "Offside", "Substitution", "Interruption"]

f = open("fullevents.csv", "r")

event_list = []
for line in f:
    event_list.append(line.split(","))



header = event_list.pop(0)
header = ",".join(header)

def playParser(ev_list, init_max):
    plays = []
    curr_game = ev_list[0][0]
    current_initiative = ev_list[0][1]
    initiative_stack = 1

    current_play = []

    for play in ev_list:


        if play[1] == current_initiative and initiative_stack < init_max:
            initiative_stack += 1

        elif play[1] != current_initiative:
            initiative_stack -= 1
        
        if initiative_stack < 1 or play[0] != curr_game or play[6] in terminals:  # we have a new initiative starting
            if len(current_play) > 5:
                plays.append(current_play)
            current_play = []
            initiative = 1
            current_initiative = play[1]
            curr_game = play[0]

        current_play.append(play)

    playnum = 0    
    for play in plays:
        f = open("play" + str(playnum), "w")
        f.write(header)
        for ev in play:
            for el in ev:
                f.write(el)
                if not "\n" in el:
                    f.write(",")
        f.close()
        playnum += 1
    return plays
playParser(event_list, 4)
        
    

