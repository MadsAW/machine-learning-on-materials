#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 14:25:16 2018

@author: Simon
"""
from ase.db import connect
import numpy as np
import matplotlib.pyplot as plt
import pickle



#Fjerner atomer hvor der kun er et grundstof
#Fjerner features hvor der er færre end (cutOff) materialer som indeholder grundstofferne


data = connect('oqmd12.db')

atomsList=[]

for row in data.select():
    atomsList.append(data.get_atoms(row['id']))

#Path to saved files
path = "Saved matrices/24-09-2018 21.37 TEST/"

featureMatrix = np.load(path+"/featureMatrix.npy")

with open(path+"/pickledEnergies.txt", "rb") as pickleFile:
    energies = pickle.load(pickleFile)
    
with open(path+"/pickledAtomicSymbolsList.txt", "rb") as pickleFile:
    atomicSymbolsList = pickle(pickleFile)

#Koden skal laves om så ovenstående 3 loadede matricer bruges i stedet for at starte det hele forfra.

atomsRemovedNotTwo=[]
atomsRemovedCutOff=[]
indicesToRemove=[]


atomicNumberCounts={}
for atom in atomsList:
    for element in atom.get_atomic_numbers():
        if element not in atomicNumberCounts:
            atomicNumberCounts[element]=1
        else:
            atomicNumberCounts[element]+=1

#Atomic number occurences as an np array, sorted by number atomic number.
plotData=np.array(sorted(atomicNumberCounts.items()))
cutOff = 350
newPlotData = plotData[plotData[:,1]>cutOff]
removedPlotData = plotData[plotData[:,1]<=cutOff]



index=0
for atom in atomsList:
    if len(atomicSymbolsList[index])!=2:
        atomsRemovedNotTwo.append(atom)
        indicesToRemove.append(index)
    elif any(elem in removedPlotData[:,0] for elem in atom.get_atomic_numbers()):
        atomsRemovedCutOff.append(atom)
        indicesToRemove.append(index)
    index+=1

newFeatureMatrix=np.delete(featureMatrix,indicesToRemove,0)
newAtomicSymbolsList = list(np.delete(atomicSymbolsList,indicesToRemove,0))

chemFormulaeNotTwo=[]
for i in range(len(atomsRemovedNotTwo)):
    chemFormulaeNotTwo.append(atomsRemovedNotTwo[i].get_chemical_formula())

print(f"Removed {len(featureMatrix)-len(newFeatureMatrix)} entries from the feature matrix")



plt.bar(newPlotData[:,0],newPlotData[:,1], color='blue')
plt.bar(removedPlotData[:,0],removedPlotData[:,1], color='red')
plt.plot([-1,max(plotData[:,0])+2],[cutOff,cutOff], color='red')
plt.show()

removedAtomicNumbers=removedPlotData[:,0]





np.save(f"featureMatrixCutoff{cutOff}_noSingleElementKrystals.npy", newFeatureMatrix)
np.save(f"atomicSymbolsListCutoff{cutOff}_noSingleElementKrystals.npy", newAtomicSymbolsList)