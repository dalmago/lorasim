
import random
import math
import numpy as np
import matplotlib.pyplot as plt

class myNode():
    def __init__(self, id):
        self.nodeId = id

        self.x = 0
        self.y = 0

        found = 0
        rounds = 0

        while found == 0 and rounds < 100:
            a = random.random()
            b = random.random()
            if b<a:
                a,b = b,a
            posx = b*maxDist*math.cos(2*math.pi*a/b)+bsx
            posy = b*maxDist*math.sin(2*math.pi*a/b)+bsy
            if len(nodes) > 0:
                for index, n in enumerate(nodes):
                    dist = np.sqrt(((abs(n.x-posx))**2)+((abs(n.y-posy))**2))
                    if dist >= 10:
                        found = 1
                        self.x = posx
                        self.y = posy
                    else:
                        rounds = rounds + 1
                        if rounds == 100:
                            print ("could not place new node %s, giving up" %(id))
                            exit(-1)
            else:
                print ("first node")
                self.x = posx
                self.y = posy
                found = 1

        self.dist = np.sqrt((self.x-bsx)*(self.x-bsx)+(self.y-bsy)*(self.y-bsy))

        global ax
        ax.add_artist(plt.Circle((self.x, self.y), 2, fill=True, color='blue'))


nrNodes = 2

# global stuff
nodes = []

# this is an array with measured values for sensitivity
# see paper, Table 1
sf7 = np.array([7,-126.5,-124.25,-120.75])
sf8 = np.array([8,-127.25,-126.75,-124.0])
sf9 = np.array([9,-131.25,-128.25,-127.5])
sf10 = np.array([10,-132.75,-130.25,-128.75])
sf11 = np.array([11,-134.5,-132.75,-128.75])
sf12 = np.array([12,-133.25,-132.25,-132.25])

# required SNR for each SF
adr_snr_req = {
    7: -7.5,
    8: -10,
    9: -12.5,
    10: -15,
    11: -17.5,
    12: -20
}

#cochannel rejection
sf7d = np.array([7, -6, 16, 18, 19, 19, 20])
sf8d = np.array([8, 24, -6, 20, 22, 22, 22])
sf9d = np.array([9, 27, 27, -6, 23, 25, 25])
sf10d = np.array([10, 30, 30, 30, -6, 26, 28])
sf11d = np.array([11, 33, 33, 33, 33, -6, 29])
sf12d = np.array([12, 36, 36, 36, 36, 36, -6])

Ptx = 14
gamma = 2.08
d0 = 40.0
Lpld0 = 127.41

sensi = np.array([sf7, sf8, sf9, sf10, sf11, sf12])

if __name__ == "__main__":
    minsensi = sensi[5, 2]
    Lpl = Ptx - minsensi  # max path loss
    maxDist = d0 * (math.e ** ((Lpl - Lpld0) / (10.0 * gamma)))

    # base station placement
    bsx = maxDist + 10
    bsy = maxDist + 10
    xmax = bsx + maxDist + 20
    ymax = bsy + maxDist + 20

    # plt.ion()
    plt.figure()
    ax = plt.gcf().gca()
    # XXX should be base station position
    ax.add_artist(plt.Circle((bsx, bsy), 3, fill=True, color='green'))
    ax.add_artist(plt.Circle((bsx, bsy), maxDist, fill=False, color='green'))

    for i in range(0,nrNodes):
        node = myNode(i)
        nodes.append(node)

    plt.xlim([0, xmax])
    plt.ylim([0, ymax])
    plt.draw()
    plt.show()

    with open("nodes_%s.csv" %(nrNodes), "w") as f:
        f.write("Id,x,y\n")

        for n in nodes:
            f.write("%s,%s,%s\n" %(n.nodeId, n.x, n.y))
