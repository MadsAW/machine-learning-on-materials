#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:46:25 2018

@author: Simon
"""
import numpy as np
import pickle
import pandas as pd
from getGroupAndPeriod import getGroupAndPeriod

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



def no_redundancy_matrix(path,featureMatrixFile,atomicSymbolsListFile):
    
    featureMatrix = np.load(path+featureMatrixFile)
        
    with open(path+atomicSymbolsListFile, "rb") as pickleFile:
        atomicSymbolsList = pickle.load(pickleFile)
    

    
    featureMatrix.shape = (featureMatrix.shape[0], -1)
    newFeatureMatrix=[]
    
    for observation in range(len(atomicSymbolsList)):
        element1 = getGroupAndPeriod(atomicSymbolsList[observation][0])
        element2 = getGroupAndPeriod(atomicSymbolsList[observation][1])
        
        
        newFeatureMatrix.append(np.hstack([element1,element2,featureMatrix[observation]]))
        
    return np.array(newFeatureMatrix)
    
    


def advanced_large_matrix(path,feature_matrix_file,atomic_symbols_list_file):
    
    feature_matrix = np.load(path+feature_matrix_file)
        

    with open(path+atomic_symbols_list_file, "rb") as pickle_file:
        atomic_symbols_list = pickle.load(pickle_file)
    
    new_feature_matrix=[]

    for observation in range(len(atomic_symbols_list)):
        grp1, prd1 = getGroupAndPeriod(atomic_symbols_list[observation][0])
        grp2, prd2 = getGroupAndPeriod(atomic_symbols_list[observation][1])
        feature=feature_matrix[observation]
        

        #23 fordi der er 17 grupper og 6 perioder i datasættet.
        element_feature=np.zeros((23,23, feature_matrix[observation].shape[-1]))
        prd1+=17
        prd2+=17
        
        #Fordi matricen er nulindekseret
        grp1-=1
        grp2-=1
        prd1-=1
        prd2-=1
        
        
        #Indsæt søjlevektor på passende steder
        element_feature[grp1,grp1]+=feature[0,0]
        element_feature[grp1,grp2]+=feature[0,1]
        element_feature[grp2,grp2]+=feature[1,1]
        element_feature[grp2,grp1]+=feature[1,0]
        
        element_feature[prd1,prd1]+=feature[0,0]
        element_feature[prd1,prd2]+=feature[0,1]
        element_feature[prd2,prd2]+=feature[1,1]
        element_feature[prd2,prd1]+=feature[1,0]
        
        element_feature[prd1,grp1]+=feature[0,0]
        element_feature[prd1,grp2]+=feature[0,1]
        element_feature[prd2,grp2]+=feature[1,1]
        element_feature[prd2,grp1]+=feature[1,0]
        
        element_feature[grp1,prd1]+=feature[0,0]
        element_feature[grp1,prd2]+=feature[0,1]
        element_feature[grp2,prd2]+=feature[1,1]
        element_feature[grp2,prd1]+=feature[1,0]
        
        
        
        
        
        
        new_feature_matrix.append(element_feature)
    
    
    
    return np.array(new_feature_matrix)


#path = "Saved matrices/04-01-2019 21.56/sorted_Cutoff25_noSingleElementKrystals/"
#feature_matrix_file = "train_featureMatrix.npy"
#atomic_symbols_list_file = "train_pickledAtomicSymbolsList.txt"
#
#
#largeFeatureMatrix = advanced_large_matrix(path,feature_matrix_file, atomic_symbols_list_file)


        