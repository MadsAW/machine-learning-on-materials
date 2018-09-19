#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 14:11:28 2018

@author: Simon
"""

from ase.db import connect
from prdf import prdf
import numpy as np
import matplotlib.pyplot as plt
import time
import os

data = connect('oqmd12.db')

atomsList=[]

for row in data.select():
    atomsList.append(data.get_atoms(row['id']))

#%%
"""

prdf returnerer et tuple med to elementer. Det andet element er en liste af grundstoffer der indgår
Første element er følgende matrix.

GS står for grundstoffets navn.

        GS1 | GS2 | GS3 ...
        -------------------

GS1|     L  |  L  |  L  |
        -----------------
GS2|     L  |  L  |  L  |
        -----------------
GS3|     L  |  L  |  L  |

...

Hvert L er en liste med fordelinger i forskellige afstande.


Som input tager prdf følgende: Atoms, rs, dr, rmax
-et Atoms objekt
-rs,  et 1D ndarray med afstande hvor fordelingsfunktionen udregnes
-dr,  For hver afstand i arrayet ovenfor udregnes tæthede af atomer inden for tykkelsen dr
-maks radius



"""
#%%

rmax = 10.0
dr = 0.2
rs = np.arange(0, rmax - dr, dr / 5)


x=np.array(prdf(atomsList[0],rs,dr,rmax)[0])

dim = [len(atomsList)]
for i in np.shape(x):
    dim.append(i)


featureMatrix=np.zeros(dim)

atomicSymbolsList = np.full(dim[0:2],"", dtype='<U3')


#%%

start = time.time()
featureMatrix=np.zeros(dim)


index=0
for atom in atomsList:
    featureMatrix[index],atomicSymbolsList[index]=prdf(atom,rs,dr,rmax)
    print(f"Progress: {index / dim[0] * 100:8.5f}%. Elapsed: {(time.time()-start)/60:5.2f} minutes. Remaining: {((time.time()-start)/ ((index +1) / dim[0]))/60 - (time.time()-start)/60:5.2f} minutes")
    index+=1

np.save(f"featureMatrix.npy", featureMatrix)

print("DONE")







#%%
#featureMatrixLoaded = np.load("Gemte matrices/featureMatrix.npy")
#featureMatrix=featureMatrixLoaded
#%%

energies = [atom.get_potential_energy() for atom in atomsList]





#%%
#Fjerner atomer hvor der kun er et grundstof
#Fjerner features hvor der er færre end (cutOff) materialer som indeholder grundstofferne

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
    if len(np.unique(atomicSymbolsList[index]))!=2:
        atomsRemovedNotTwo.append(atom)
        indicesToRemove.append(index)
    elif any(elem in removedPlotData[:,0] for elem in atom.get_atomic_numbers()):
        atomsRemovedCutOff.append(atom)
        indicesToRemove.append(index)
    index+=1

newFeatureMatrix=np.delete(featureMatrix,indicesToRemove,0)
newAtomicSymbolsList = np.delete(atomicSymbolsList,indicesToRemove,0)

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
