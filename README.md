# LoRaSim
> Modified version from http://www.lancaster.ac.uk/scc/sites/lora/lorasim.html

LoRaSim consist of four Python scripts: loraDir.py, loraDirMulBs.py, directionalLoraIntf.py, and oneDirectionalLoraIntf.py.
loraDir.py simulates a single base station, loraDirMulBs.py simulates more than one base station (up to 24), directionalLoraIntf simulates nodes with directional antennae and multiple networks, oneDirectionalLoraIntf.py simulates base stations with directional antennae and mulitple networks.
All require the following packages: matplotlib, simpy and numpy.

## Usage
All simulators operate mostly in the same way, and take the same parameters. The main difference is that loraDirMulBS.py simulates up to 24 basestations, and xx takes.

loraDir.py \<NODES> \<AVGSEND> \<EXPERIMENT> \<SIMTIME> [COLLISION]

loraDirMulBS.py \<NODES> \<AVGSEND> \<EXPERIMENT> \<SIMTIME> \<BASESTATIONS> [COLLISION]

directionalLoraIntf.py \<NODES> \<AVGSEND> \<EXPERIMENT> \<SIMTIME> \<BASESTATIONS> \<COLLISION> \<DIRECTIONALITY> \<NETWORKS> \<BASEDIST>

oneDirectionalLoraIntf.py \<NODES> \<AVGSEND> \<EXPERIMENT> \<SIMTIME> \<BASESTATIONS> \<COLLISION> \<DIRECTIONALITY> \<NETWORKS> \<BASEDIST>

### Description

#### NODES
number of nodes to simulate.

#### AVGSEND
average sending interval in milliseconds.

#### EXPERIMENT
experiment is an integer that determines with what radio settings the simulation is run. All nodes are configured with a fixed transmit power and a single transmit frequency, unless stated otherwise.

##### 0
use the settings with the the slowest datarate (SF12, BW125, CR4/8).

##### 1
similar to experiment 0, but use a random choice of 3 transmit frequencies.

##### 2
use the settings with the fastest data rate (SF6, BW500, CR4/5).

##### 3
optimise the setting per node based on the distance to the gateway.

##### 4
use the settings as defined in LoRaWAN (SF12, BW125, CR4/5).

##### 5
similar to experiment 3, but also optimises the transmit power.

#### SIMTIME
total running time in milliseconds.

#### BASESTATIONS
number of base stations to simulate. Can be either 1, 2, 3, 4, 6, 8 or 24.

#### COLLISION
set to 1 to enable the full collision check, 0 to use a simplified check (default). With the simplified check, two messages collide when they arrive at the same time, on the same frequency and spreading factor. The full collision check considers the ‘capture effect’, whereby one of the two colliding message may still pass depending on the relative timing and difference in receive power.

#### DIRECTIONALITY
set to 1 to enable directional antennae for nodes.

#### NETWORKS
number of LoRa networks.

#### BASEDIST
X-distance between two base stations.

### Output

The result of every simulation run will be appended to a file named expX.dat, whereby X is the experiment number. The file contains a space separated table of values for nodes, collisions, transmissions and total energy spent. The data file can be easily plotted using e.g. gnuplot.

# License
LoRaSim - Copyright (c) 2016-2017 Thiemo Voigt and Martin Bor. This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.
