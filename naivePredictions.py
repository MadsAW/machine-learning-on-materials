#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 18:15:16 2018

@author: Simon
"""

import numpy as np
from ase.db import connect
import pandas as pd


data = connect('oqmd12.db')

atomsList=[]

for row in data.select():
    atomsList.append(data.get_atoms(row['id']))
    

chemicalSymbols=[]
energies=[]

for atom in atomsList:
    chemicalSymbols.append(atom.get_chemical_symbols())
    energies.append(atom.get_potential_energy())



atomicSymbolsAndNumbers=np.array(pd.read_csv("atomicSymbolsAndNumbers.csv", header=None, sep=","))
def getAtomicNumbers(atomicSymbols):
    out=[]
    for elem in atomicSymbols:
        for i in atomicSymbolsAndNumbers:
            if elem == i[1]:
                out.append(i[0])
    
    return(out)
    
    
indicesToRemove=[]

atomicNumberCounts={}
for crystal in chemicalSymbols:
    for element in list(np.unique(getAtomicNumbers(crystal))):
        if element not in atomicNumberCounts:
            atomicNumberCounts[element]=1
        else:
            atomicNumberCounts[element]+=1

#Atomic number occurences as an np array, sorted by number atomic number.
allSymbols=np.array(sorted(atomicNumberCounts.items()))
cutOff = 25
removedSymbols = allSymbols[allSymbols[:,1]<=cutOff]



index=0
for crystal in chemicalSymbols:
    if len(list(np.unique(getAtomicNumbers(crystal))))!=2:
        indicesToRemove.append(index)
    elif any(elem in removedSymbols[:,0] for elem in getAtomicNumbers(crystal)):
        indicesToRemove.append(index)
    index+=1


chemicalSymbols = list(np.delete(chemicalSymbols,indicesToRemove,0))
energies = list(np.delete(energies,indicesToRemove,0))






#Mean
mean=np.mean(energies)

a=0
for i in range(len(energies)):
    a+=(energies[i]-mean)**2
rmse_a=np.sqrt(a/len(energies))








#Linear model, linear algebra, least squares method
chemicalSymbolsCount = []

for crystal in chemicalSymbols:
    elements, counts = np.unique(crystal, return_counts=True)
    chemicalSymbolsCount.append([list(elements), list(counts)])
    
    

uniqueAtomicSymbols=[]
for i in chemicalSymbolsCount:
    for j in i[0]:
        uniqueAtomicSymbols.append(j)
            
uniqueAtomicSymbols = list(np.unique(uniqueAtomicSymbols))
    
mappedAtomicNumber={}
index=0
for sym in uniqueAtomicSymbols:
    mappedAtomicNumber[sym]=index
    index+=1


A=np.zeros((len(chemicalSymbolsCount),len(mappedAtomicNumber)))
B=energies

index=0
for i in chemicalSymbolsCount:
    A[index][mappedAtomicNumber[i[0][0]]]=i[1][0]
    A[index][mappedAtomicNumber[i[0][1]]]=i[1][1]
    
    index+=1



result = np.linalg.lstsq(A,B)




b=0
for i in range(len(energies)):
    b+=(energies[i]-sum((A[i]*result[0])))**2
rmse_b=np.sqrt(b/len(energies))



print(f"\n\nGuess mean every time. Root mean square error {rmse_a:.3f} eV.\n")# =57.436 eV
print(f"For crystal 3F4H guess 3*a_F+4*a_H. a's found least squares regression. Root mean square error {rmse_b:.3f} eV\n\n")# =9.022 eV