#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 21:46:40 2018

@author: Simon
"""

import numpy as np
import pickle
import pandas as pd

path = "Saved matrices/11-10-2018 11.36/sorted_Cutoff25_noSingleElementKrystals/"

all_counts={}
for dataset in ['train','validate','test','FullSet']:
    
    
    featureMatrixFile = dataset+"_featureMatrix.npy"
    atomicSymbolsListFile = dataset+"_pickledAtomicSymbolsList.txt"
    energiesFile = dataset+"_pickledEnergies.txt"
    
    
    
    featureMatrix = np.load(path+featureMatrixFile)
        
    with open(path+atomicSymbolsListFile, "rb") as pickleFile:
        atomicSymbolsList = pickle.load(pickleFile)
    
    
    atomicSymbolsAndNumbers=np.array(pd.read_csv("atomicSymbolsAndNumbers.csv", header=None, sep=","))
    def getAtomicNumbers(atomicSymbols):
        out=[]
        for elem in atomicSymbols:
            for i in atomicSymbolsAndNumbers:
                if elem == i[1]:
                    out.append(i[0])
        
        return(out)
    
    
    
    
    AtomicSymbols=[]
    for i in atomicSymbolsList:
        for j in i:
            AtomicSymbols.append(j)
            
    uniqueAtomicNumbers = list(np.unique(AtomicSymbols))
    
    
    AtomicNumberCounts={}
    
    for element in uniqueAtomicNumbers:
        AtomicNumberCounts[element]=AtomicSymbols.count(element)

    all_counts[dataset]=AtomicNumberCounts
    
    
for dataset in ['train','validate','test']:
    for element in all_counts[dataset]:
        all_counts[dataset][element]=round( 100*all_counts[dataset][element]/all_counts['FullSet'][element],1)
        
#FullSet er i antal
#De tre andre sæt er i pct
