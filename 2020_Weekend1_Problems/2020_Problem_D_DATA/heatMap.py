#File for generating heat maps for events you want.

import statistics
import numpy as np
import matplotlib.pyplot as plt

#Function will separate data based on the column number given, into files where the column names that
#had spaces now have _ in the file name.
def localize(playname, colnum):
    f = open(playname, "r")

    for line in f:
        linesplt = line.rstrip("\n").split(",")
        actionType = open("data/events/"+str(linesplt[colnum].replace(" ", "_"))+".csv", "a")
        actionType.write(line)
        actionType.close()

    f.close()


def heat_map(eventType, ourTeam):
    plt.ylabel('Y-axis')
    plt.xlabel('X-axis')

    heatMPSrc = np.zeros((101,101))
    heatMPDst = np.zeros((101,101))

    f = open("data/events/"+str(eventType))
    for line in f:
        linesplt = line.split(",")
        if ourTeam and linesplt[1] == "Huskies":
            heatMPSrc[int(float(linesplt[9]))][int(float(linesplt[8]))] += 1
            heatMPDst[int(float(linesplt[11].rstrip("\n")))][int(float(linesplt[10]))] += 1

    plt.imshow(heatMPDst, cmap='inferno', interpolation="gaussian")
    plt.show()
    plt.imshow(heatMPSrc, cmap='inferno', interpolation="gaussian")
    plt.show()
    f.close()



def plotEvents(eventType, ourTeam):
    plt.ylabel('Y-axis')
    plt.xlabel('X-axis')

    f = open("data/events/"+str(eventType))
    for line in f:
        linesplt = line.split(",")
        print(float(linesplt[8]), float(linesplt[9]))
        if ourTeam and linesplt[1] == "Huskies":
            plt.plot(float(linesplt[8]), float(linesplt[9]), 'go')
            plt.plot(float(linesplt[10]), float(linesplt[11].rstrip("\n")), 'g^')
        #else:
            #plt.plot(float(linesplt[8]), float(linesplt[9]), 'ro')
            #plt.plot(float(linesplt[10]), float(linesplt[11].rstrip("\n")), 'r^')

    f.close()
    plt.show()

if __name__ == "__main__":
    heat_map("Cross.csv", True)



