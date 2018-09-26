#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:46:25 2018

@author: Simon
"""
import numpy as np
import pickle
import pandas as pd

def simpleLargeMatrix(path,featureMatrixFile,atomicSymbolsListFile):
    
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
    
    
    
    
    uniqueAtomicSymbols=[]
    for i in atomicSymbolsList:
        for j in i:
            uniqueAtomicSymbols.append(j)
    
    uniqueAtomicNumbers = list(np.sort(getAtomicNumbers(np.unique(uniqueAtomicSymbols))))
    
    mappedAtomicNumber={}
    index=0
    for num in uniqueAtomicNumbers:
        mappedAtomicNumber[num]=index
        index+=1
        
        
        
    newFeatureMatrix=np.zeros((len(featureMatrix),len(mappedAtomicNumber),len(mappedAtomicNumber),len(featureMatrix[0,0,0])))

    
    materialNum = 0
    for matrix in featureMatrix:
        newIndex0 = mappedAtomicNumber[getAtomicNumbers(atomicSymbolsList[materialNum])[0]]
        newIndex1 = mappedAtomicNumber[getAtomicNumbers(atomicSymbolsList[materialNum])[1]]
        
        
        newFeatureMatrix[materialNum,newIndex0,newIndex0] = matrix[0,0]
        newFeatureMatrix[materialNum,newIndex1,newIndex0] = matrix[1,0]
        newFeatureMatrix[materialNum,newIndex0,newIndex1] = matrix[0,1]
        newFeatureMatrix[materialNum,newIndex1,newIndex1] = matrix[1,1]
        
        
    
        materialNum += 1
        
        
    return newFeatureMatrix, mappedAtomicNumber
    
    
    
        
        
        
        