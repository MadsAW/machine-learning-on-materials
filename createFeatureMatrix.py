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

atomicSymbolsList = []


#%%

start = time.time()
featureMatrix=np.zeros(dim)


index=0
for atom in atomsList:
    X=prdf(atom,rs,dr,rmax)
    featureMatrix[index] = X[0]
    atomicSymbolsList.append(X[1])
    print(f"Progress: {index / dim[0] * 100:8.5f}%. Elapsed: {(time.time()-start)/60:5.2f} minutes. Remaining: {((time.time()-start)/ ((index +1) / dim[0]))/60 - (time.time()-start)/60:5.2f} minutes")
    index+=1

np.save(f"featureMatrix.npy", featureMatrix)
energies = [atom.get_potential_energy() for atom in atomsList]

#HUSK AT TILFØJE SÅ atomicSymbolsList GEMMES I EN ANDEN FIL
#HUSK AT TILFØJE SÅ energies GEMMES I EN ANDEN FIL

print("DONE")







