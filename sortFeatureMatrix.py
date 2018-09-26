#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 14:25:16 2018

@author: Simon
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import os



#Fjerner atomer hvor der kun er et grundstof
#Fjerner features hvor der er færre end (cutOff) materialer som indeholder grundstofferne


atomicSymbolsAndNumbers=np.array(pd.read_csv("atomicSymbolsAndNumbers.csv", header=None, sep=","))
def getAtomicNumbers(atomicSymbols):
    out=[]
    for elem in atomicSymbols:
        for i in atomicSymbolsAndNumbers:
            if elem == i[1]:
                out.append(i[0])
    
    return(out)



#Path to saved files
path = "Saved matrices/24-09-2018 21.44/"

featureMatrix = np.load(path+"/featureMatrix.npy")

with open(path+"/pickledEnergies.txt", "rb") as pickleFile:
    energies = pickle.load(pickleFile)
    
with open(path+"/pickledAtomicSymbolsList.txt", "rb") as pickleFile:
    atomicSymbolsList = pickle.load(pickleFile)


crystalsRemovedNotTwo=[]
crystalsRemovedCutOff=[]
indicesToRemove=[]


atomicNumberCounts={}
for crystal in atomicSymbolsList:
    for element in getAtomicNumbers(crystal):
        if element not in atomicNumberCounts:
            atomicNumberCounts[element]=1
        else:
            atomicNumberCounts[element]+=1

#Atomic number occurences as an np array, sorted by number atomic number.
plotData=np.array(sorted(atomicNumberCounts.items()))
cutOff = 25
newPlotData = plotData[plotData[:,1]>cutOff]
removedPlotData = plotData[plotData[:,1]<=cutOff]



index=0
for crystal in atomicSymbolsList:
    if len(atomicSymbolsList[index])!=2:
        crystalsRemovedNotTwo.append(crystal)
        indicesToRemove.append(index)
    elif any(elem in removedPlotData[:,0] for elem in getAtomicNumbers(crystal)):
        crystalsRemovedCutOff.append(crystal)
        indicesToRemove.append(index)
    index+=1

newFeatureMatrix=np.delete(featureMatrix,indicesToRemove,0)
newAtomicSymbolsList = list(np.delete(atomicSymbolsList,indicesToRemove,0))
newEnergies = list(np.delete(energies,indicesToRemove,0))

print(f"Removed {len(featureMatrix)-len(newFeatureMatrix)} entries from the feature matrix")



plt.bar(newPlotData[:,0],newPlotData[:,1], color='blue')
plt.bar(removedPlotData[:,0],removedPlotData[:,1], color='red')
plt.plot([-1,max(plotData[:,0])+2],[cutOff,cutOff], color='red')
plt.show()




try:
    os.mkdir(path+f"sorted_Cutoff{cutOff}_noSingleElementKrystals/")
except:
    pass
newFolder=path+f"sorted_Cutoff{cutOff}_noSingleElementKrystals/"

np.save(newFolder+"featureMatrix.npy", newFeatureMatrix)

with open(newFolder+"/pickledEnergies.txt", "wb") as pickleFile:
    pickle.dump(newEnergies, pickleFile)
    
with open(newFolder+"/pickledAtomicSymbolsList.txt", "wb") as pickleFile:
    pickle.dump(newAtomicSymbolsList, pickleFile)
    
print("DONE")