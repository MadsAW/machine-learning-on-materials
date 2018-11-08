#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 13:54:00 2018

@author: Simon
"""


import os
from createLargerFeatureMatrix import simpleLargeMatrix
import pickle
import numpy as np

path = "Saved matrices/11-10-2018 11.36/sorted_Cutoff25_noSingleElementKrystals/"
featureMatrixFile = "train_featureMatrix.npy"
atomicSymbolsListFile = "train_pickledAtomicSymbolsList.txt"
energiesFile = "train_pickledEnergies.txt"

largeFeatureMatrix, mappedAtomicNumber = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)


with open(path+energiesFile, "rb") as pickleFile:
    energies = pickle.load(pickleFile)

largeFeatureMatrix.shape = (largeFeatureMatrix.shape[0], -1)

X = largeFeatureMatrix
Y = np.array(energies)





X=np.array([[1,2,3],[4,5,6],[7,8,9]])
Y=np.array([10,11,12])




lam = 3
I = np.identity(len(X))

c=1
def f(xi,xj):
    return (xi @ xj)+c

K = np.zeros(X.shape)
for i in range(0,int(np.ceil(len(X)/2))+1):
    for j in range(0,int(np.ceil(len(X)/2))+1):
        K[i,j] = f(X[i],X[j])
        K[j,i] = f(X[i],X[j])



diff=[]

for i in range(len(X)):
    x=X[i]
    kap = np.zeros(x.shape)
    for i in range(len(X)):
        kap[i] = f(X[i],x)
        
    y=(Y.T @ np.linalg.inv(np.matrix(K+lam*I)) @ kap)
    
    diff.append((Y[i]-y)[0,0])









#Load validation set
featureMatrixFileValidate = "validate_featureMatrix.npy"
atomicSymbolsListFileValidate = "validate_pickledAtomicSymbolsList.txt"
energiesFileValidate = "validate_pickledEnergies.txt"

largeFeatureMatrixValidate, mappedAtomicNumberValidate = simpleLargeMatrix(path,featureMatrixFileValidate, atomicSymbolsListFileValidate)


with open(path+energiesFileValidate, "rb") as pickleFile:
    energiesValidate = pickle.load(pickleFile)

largeFeatureMatrixValidate.shape = (largeFeatureMatrixValidate.shape[0], -1)

X_v = largeFeatureMatrixValidate
Y_v = np.array(energiesValidate)




"""
#Make predictions on validation set

predictionsValidate = model.predict(X_v)
a=0
for i in range(len(predictionsValidate)):
    a+=(energiesValidate[i]-predictionsValidate[i])**2
rmseValidate=np.sqrt(a/len(energiesValidate))

print("RMSE on validation data "+str(rmseValidate))







print("DONE")
"""