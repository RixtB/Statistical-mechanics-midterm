from mpmath import *
import numpy as np
import math
import matplotlib.pyplot as plt
mp.dps = 15; mp.pretty = True

#for plotting with readable axis lables
font = {'family': 'Arial',
        'weight': 'normal',
        'size': 14}
plt.rc('font', **font)

#defining variables
k = 1.380649*10**-23                        #boltzmann's constant
eV = 1.60217*10**-19                        #converting from eV to joules
Temp = 5800                                 #5800 for earth, 9940 for Sirius A
step = 0.05                                 #stepsize in energie for the plot

#function efficiency takes bandgap in eV and temparature in K and outputs the efficiency of the solar cell
def efficiency(Egap,T):
    y = Egap * eV / (k*T)                   #defining a unitness parameter for Egap
    numerator = y*(2*y*polylog(2,exp(-y))+2*polylog(3,exp(-y))-y**2*(log(1-exp(-y))))
    denumerator = math.pi**4 / 15
    return numerator / denumerator


#function n_absorbed takes bandgap in eV and temparature in K and outputs the fraction of absorbed photons by the solar cell
def efficiencyTandem(Egap1,Egap2,T):        #Egap1 > Egap2
    y1 = Egap1 * eV / (k*T)
    y2 = Egap2 * eV/ (k*T)
    contributionGap1 = (2*y1*polylog(2,exp(-y1))+2*polylog(3,exp(-y1))-y1**2*(log(1-exp(-y1))))*y1
    contributionGap2 = ((2*y2*polylog(2,exp(-y2))+2*polylog(3,exp(-y2))-y2**2*(log(1-exp(-y2))))-(2*y1*polylog(2,exp(-y1))+2*polylog(3,exp(-y1))-y1**2*(log(1-exp(-y1)))))*y2
    numerator = contributionGap1 + contributionGap2
    denumerator = math.pi**4 / 15
    return numerator / denumerator

#forming an array of bandgap energies and calculating efficieny for each energy
energies = np.arange(0.05, 5, step)
efficiencies = np.zeros(len(energies))                  #creating empty arrays for efficiencies: single layer device
efficienciesTandemBelow = np.zeros(len(energies))       #for tandem device with the Si as top layer
efficienciesTandemAbove = np.zeros(len(energies))       #for tandem device with the Si as bottom layer
for i in energies:                                      #writing each efficiency in the arrays
    number = np.where(energies == i)
    efficiencies[number] = efficiency(i, Temp)
    efficienciesTandemBelow[number] = efficiencyTandem(i, 1.12, Temp)
    efficienciesTandemAbove[number] = efficiencyTandem(1.12, i, Temp)

#finding maximal efficinecy and at which bandgap this occurs
max_eff = np.amax(efficiencies)
energie_max = energies[np.where(efficiencies== max_eff)]
print("The maximum efficiency occurs at a bandgap energy of " + str(energie_max[0]) +" eV and is " + str(round(max_eff,3)*100) + " percent for a single junciton device.")


max_eff = np.amax(efficienciesTandemBelow)
energie_max = energies[np.where(efficienciesTandemBelow == max_eff)]
print("The maximum efficiency occurs at a bandgap energy of " + str(energie_max[0]) +" eV and is " + str(round(max_eff,3)*100) + " percent for a tandem device with the Si on top.")

max_eff = np.amax(efficienciesTandemAbove)
energie_max = energies[np.where(efficienciesTandemAbove == max_eff)]
print("The maximum efficiency occurs at a bandgap energy of " + str(energie_max[0]) +" eV and is " + str(round(max_eff,3)*100) + " percent for a tandem device with the Si on top.")

#plotting energies and efficiencies for single layer and tandem devices
plt.plot(energies, efficiencies*100)
#plt.plot(energies, efficienciesTandemAbove*100)
#plt.plot(energies, efficienciesTandemBelow*100)
plt.xlabel('Bandgap energie (eV)')
plt.ylabel('Efficiency (%)')
plt.legend(['Single cell', 'Tandem, Si on top', 'Tandem, Si on bottom'])
plt.tight_layout()
plt.show()

