from multiprocessing import Process
from loraDir import run as runSim

der = []
energy = []

for i in range(100):
    x, y = runSim(4, nNodes=100)

    der.append(x)
    energy.append(y)

print("der:", der)
print("energy:", energy)
print("avg der:", sum(der)/len(der))
print("avg energy:", sum(energy)/len(energy))
