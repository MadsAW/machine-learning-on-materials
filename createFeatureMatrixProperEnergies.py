#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 14:11:28 2018

@author: Simon
"""

from ase.db import connect
from prdf import prdf
import numpy as np
import time
import datetime
import pickle
import os


data = connect('oqmd12.db')

energies = []
atomsList=[]

for row in data.select():
    atomsList.append(data.get_atoms(row['id']))
    energies.append(row.de)
    
    
now = datetime.datetime.now()
folderName = now.strftime("%d-%m-%Y %H.%M")
os.mkdir("Saved matrices/"+folderName)
#%%
"""

prdf returnerer et tuple med to elementer. Det andet element er en liste af grundstoffer der indgår
Første element er følgende matrix.

GS står for grundstoffets navn.

        GS1 | GS2 | 
        -----------

GS1|     L  |  L  |
        -----------
GS2|     L  |  L  |   
        -----------


...

Hvert L er en liste med fordelinger i forskellige afstande.


Som input tager prdf følgende: Atoms, rs, dr, rmax
-et Atoms objekt
-rs,  et 1D ndarray med afstande hvor fordelingsfunktionen udregnes
-dr,  For hver afstand i arrayet ovenfor udregnes tæthede af atomer inden for tykkelsen dr
-maks radius



"""
#%%

rmax = 6.0
dr = 0.25
rs = np.arange(0, rmax - dr, dr/5)


x=np.array(prdf(atomsList[0],rs,dr,rmax)[0])

dim = [len(atomsList)]
for i in np.shape(x):
    dim.append(i)


featureMatrix=np.zeros(dim)

atomicSymbolsList = []


#%%

start = time.time()
featureMatrix=np.zeros(dim)



index=0
for atom in atomsList:
    X=prdf(atom,rs,dr,rmax)
    featureMatrix[index] = X[0]
    atomicSymbolsList.append(X[1])
    print(f"\rProgress: {index / dim[0] * 100:8.5f}%. Elapsed: {(time.time()-start)/60:5.2f} minutes. Remaining: {((time.time()-start)/ ((index +1) / dim[0]))/60 - (time.time()-start)/60:5.2f} minutes")
    index+=1

np.save("Saved matrices/"+folderName+"/featureMatrix.npy", featureMatrix)




with open("Saved matrices/"+folderName+"/pickledEnergies.txt", "wb") as pickleFile:
    pickle.dump(energies, pickleFile)
    
with open("Saved matrices/"+folderName+"/pickledAtomicSymbolsList.txt", "wb") as pickleFile:
    pickle.dump(atomicSymbolsList, pickleFile)

print("DONE")







