#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 11:13:19 2018

@author: Simon
"""
import pandas as pd
import numpy as np

atomicSymbolsAndNumbers=np.array(pd.read_csv("atomicSymbolsAndNumbers.csv", header=None, sep=","))

def getAtomicNumbers(atomicSymbols):
    out=[]
    for elem in atomicSymbols:
        for i in atomicSymbolsAndNumbers:
            if elem == i[1]:
                out.append(i[0])
    
    return(out)

csv=pd.read_csv("groups_and_periods.csv",delimiter=";", encoding="utf8", header=0)
Z, group, period=list(csv['Z']), list(csv['Group']), list(csv['Period'])
def getGroupAndPeriod(atomicNumber):
    if atomicNumber in Z:
        return group[Z.index(atomicNumber)], period[Z.index(atomicNumber)]
    elif getAtomicNumbers([atomicNumber])[0] in Z:
        return group[Z.index(getAtomicNumbers([atomicNumber])[0])], period[Z.index(getAtomicNumbers([atomicNumber])[0])]
    else:
        print(atomicNumber)
        return None
    

