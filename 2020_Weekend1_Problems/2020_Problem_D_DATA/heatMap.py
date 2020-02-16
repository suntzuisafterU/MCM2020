#File for generating heat maps for events you want.

import statistics
import numpy as np
import matplotlib.pyplot as plt
import sys as sys

#Function will separate data based on the column number given, into files where the column names that
#had spaces now have _ in the file name.
def localize(filename, colnum):
    f = open(filename, "r")

    for line in f:
        linesplt = line.rstrip("\n").split(",")
        actionType = open("data/events/"+str(linesplt[colnum].replace(" ", "_"))+".csv", "a")
        actionType.write(line)
        actionType.close()

    f.close()


def heat_map(eventType):
    plt.ylabel('Y-axis')
    plt.xlabel('X-axis')

    heatMPSrc = np.zeros((101,101))
    heatMPDst = np.zeros((101,101))

    f = open("data/events/"+str(eventType))
    for line in f:
        linesplt = line.split(",")
        heatMPSrc[int(float(linesplt[9]))][int(float(linesplt[8]))] += 1
        heatMPDst[int(float(linesplt[11].rstrip("\n")))][int(float(linesplt[10]))] += 1

    print("Generating Src Graph.")
    plt.imshow(heatMPDst, cmap='inferno', interpolation="gaussian")
    plt.show()

    print("Generating Dest Graph.")
    plt.imshow(heatMPSrc, cmap='inferno', interpolation="gaussian")
    plt.show()
    f.close()



def plotEvents(eventType):
    plt.ylabel('Y-axis')
    plt.xlabel('X-axis')

    f = open("data/events/"+str(eventType))
    for line in f:
        linesplt = line.split(",")
        plt.plot(float(linesplt[8]), float(linesplt[9]), 'go')
        plt.plot(float(linesplt[10]), float(linesplt[11].rstrip("\n")), 'g^')

    f.close()
    plt.show()

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        printf("Expected 2 options. The choice of graph (heat or norm) and which event we want to graph.")
        exit()
    if(sys.argv[1] == "heat"):
        heat_map(sys.argv[2])
    elif(sys.argv[1] == "norm"):
        plotEvents(sys.argv[2])
    else:
        print("Did you mean heat or norm?")
    exit()



