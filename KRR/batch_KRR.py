#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 14:40:54 2018

@author: Simon
"""
def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from createLargerFeatureMatrix import simpleLargeMatrix, advanced_large_matrix
from KRR_class import KernelRidgeRegression
import pickle
import numpy as np
import numpy

#Kernel matrices output folder
folder = "KRR/Saved/Run 4/"


if len(sys.argv)!=6:
    print('Usage: \n"python3 KRR_script.py method"\nwhere method is one of linear polynomial gaussian laplacian')
    sys.exit(1)

method=sys.argv[1]
lambd=float(sys.argv[2])
Feature=str(sys.argv[3])
prdf=str(sys.argv[4])
Args=float(sys.argv[5])

filename=str(prdf)

if prdf=="default":path = "Saved matrices/03-01-2019 11.04/sorted_Cutoff25_noSingleElementKrystals/"
elif prdf=="faulty": path = "Saved matrices/11-10-2018 11.36/sorted_Cutoff25_noSingleElementKrystals/"
elif prdf=="newest": path = "Saved matrices/04-01-2019 21.56/sorted_Cutoff25_noSingleElementKrystals/"
elif prdf=="deep": path = "Saved matrices/09-01-2019 16.03/sorted_Cutoff25_noSingleElementKrystals/"
#%% Load training data
featureMatrixFile = "train_featureMatrix.npy"
atomicSymbolsListFile = "train_pickledAtomicSymbolsList.txt"
energiesFile = "train_pickledEnergies.txt"

if Feature=="SimpleLarge":
    largeFeatureMatrix = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)
    folder=folder+"SimpleLarge/"
elif Feature=="GP":
    largeFeatureMatrix = advanced_large_matrix(path,featureMatrixFile, atomicSymbolsListFile)
    folder=folder+"GP/"

with open(path+energiesFile, "rb") as pickleFile:
    energies = pickle.load(pickleFile)

largeFeatureMatrix.shape = (largeFeatureMatrix.shape[0], -1)

X = largeFeatureMatrix
Y = np.array(energies)

#%% Load  Validation data

featureMatrixFileValidate = "validate_featureMatrix.npy"
atomicSymbolsListFileValidate = "validate_pickledAtomicSymbolsList.txt"
energiesFileValidate = "validate_pickledEnergies.txt"
if Feature=="SimpleLarge":
    largeFeatureMatrixValidate = simpleLargeMatrix(path,featureMatrixFileValidate, atomicSymbolsListFileValidate)
elif Feature=="GP":
    largeFeatureMatrixValidate = advanced_large_matrix(path,featureMatrixFileValidate, atomicSymbolsListFileValidate)

with open(path+energiesFileValidate, "rb") as pickleFile:
    energiesValidate = pickle.load(pickleFile)

largeFeatureMatrixValidate.shape = (largeFeatureMatrixValidate.shape[0], -1)

Xv = largeFeatureMatrixValidate
Yv = np.array(energiesValidate)

if method=='linear':
    folder=folder+"lin/"
    KRR=KernelRidgeRegression(type="linear")
    KRR.set_var(c1=Args, lambd=lambd)
    KRR.fit(X,Y, "error")
    out1=KRR.rmse
    KRR.predict(Xv,Yv)
    out2=KRR.rmse
    print("\nTrain: " + str(out1) + " Validation: " + str(out2)+"\n", flush=True)
elif method=='polynomial':
    try:
        KRR=KernelRidgeRegression(type="poly")
        KRR.set_var(c1=c1_list[c1],c2=c2_list[c2],d=d_list[d], lambd=lambd)
        KRR.fit(X,Y, "error")
        out1=KRR.rmse
        KRR.predict(Xv,Yv)
        out2=KRR.rmse
        print("\nTrain: " + str(out1) + " Validation: " + str(out2)+"\n", flush=True)
    except numpy.linalg.linalg.LinAlgError:
        out1=-1
        out2=-1
if method=='gaussian':
    folder=folder+"gauss/"
    KRR=KernelRidgeRegression(type="gauss")
    KRR.set_var(sigma=Args, lambd=lambd)
    KRR.fit(X,Y, "error")
    out1=KRR.rmse
    KRR.predict(Xv,Yv)
    out2=KRR.rmse
    print("\nTrain: " + str(out1) + " Validation: " + str(out2)+"\n", flush=True)
elif method=='laplacian':
    folder=folder+"laplace/"
    KRR=KernelRidgeRegression(type="laplace")
    KRR.set_var(sigma=Args, lambd=lambd)
    KRR.fit(X,Y, "error")
    out1=KRR.rmse
    KRR.predict(Xv,Yv)
    out2=KRR.rmse
    print("\nTrain: " + str(out1) + " Validation: " + str(out2)+"\n", flush=True)
with open(folder+filename+".csv", "a") as myfile:
    myfile.write(str(lambd)+", "+str(Args)+", "+str(out1)+", "+str(out2)+"\n")
