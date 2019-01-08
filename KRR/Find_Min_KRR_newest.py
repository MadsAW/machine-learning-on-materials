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


if len(sys.argv)!=3:
    print('Usage: \n"python3 KRR_script.py method"\nwhere method is one of linear polynomial gaussian laplacian')
    sys.exit(1)

method=sys.argv[1]
Feature=str(sys.argv[2])



path ="Saved matrices/04-01-2019 21.56/sorted_Cutoff25_noSingleElementKrystals/"
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



c_list = [10**n for n in range(-9,9)]
x = [-10**n for n in range(-9,9)]
x.reverse()
c_list = x + c_list
if method=='linear':
    output=[]
    folder=folder+"lin/"
    prev=100
    lambd=0.01
    inistep=1
    precision=0.00001
    i=0
    steps=0
    diff=100
    maxstep=1000
    while(abs(diff)>precision and steps<maxstep):
        GoodDir=True
        div=2**i
        step=inistep/div
        while (GoodDir):
            steps+=1
            lambd=lambd+step*(-1)**i
            KRR=KernelRidgeRegression(type="linear")
            KRR.set_var(c1=-10**10, lambd=lambd)
            KRR.fit(X,Y)
            KRR.predict(Xv,Yv)
            out2=KRR.rmse
            diff=prev-out2
            if diff<0:
                GoodDir=False
            prev=out2
            output.append([lambd,out2])
            print("\nLambda: " + str(lambd) + " Validation: " + str(out2)+"\n", flush=True)
        i+=1



    with open(folder + "MINI_other_LIN_newest", 'wb') as file:
        pickle.dump([output], file)







c1_list = list(frange(-20,-5,2))

c2_list = list(frange(-40,-15,2.5))

d_list = list(range(1,7,1))

if method=='polynomial':
    out1_matrix_pol = np.zeros((len(c1_list), len(c2_list), len(d_list)))
    out2_matrix_pol = np.zeros((len(c1_list), len(c2_list), len(d_list)))
    for c1 in range(len(c1_list)):
        for c2 in range(len(c2_list)):
            for d in range(len(d_list)):
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
                    print('singular matrix error', flush=True)
                    try:
                        KRR=KernelRidgeRegression(type="poly")
                        KRR.set_var(c1=c1_list[c1],c2=c2_list[c2],d=d_list[d], lambd=lambd)
                        KRR.fit(X,Y, "error")
                        out1=KRR.rmse
                        KRR.predict(Xv,Yv)
                        out2=KRR.rmse
                        print("\nTrain: " + str(out1) + " Validation: " + str(out2)+"\n", flush=True)
                    except:
                        pass
                except:
                    pass
                out1_matrix_pol[c1,c2,d]=out1
                out2_matrix_pol[c1,c2,d]=out2

    with open(folder + "3_pol_train", 'wb') as file:
        pickle.dump([lam_list, c1_list, c2_list, d_list, out1_matrix_pol], file)
    with open(folder + "3_pol_val", 'wb') as file:
        pickle.dump([lam_list, c1_list, c2_list, d_list, out2_matrix_pol], file)






if method=='gaussian':
    folder=folder+"gauss/"
    output=[]
    prev=100
    sigma=1
    inistep=5
    precision=0.00001
    i=0
    steps=0
    maxstep=250
    diff=100
    while(abs(diff)>precision and steps<maxstep):
        GoodDir=True
        div=2**i
        step=inistep/div
        while (GoodDir):
            steps+=1
            sigma=sigma+step*(-1)**i
            KRR=KernelRidgeRegression(type="gauss")
            KRR.set_var(sigma=sigma, lambd=0.01)
            KRR.fit(X,Y,"error")
            out1=KRR.rmse
            KRR.predict(Xv,Yv)
            out2=KRR.rmse
            diff=prev-out1
            if diff<0:
                GoodDir=False
            prev=out1
            output.append([sigma,out1,out2])
            print("\nSigma: " + str(sigma) + " Train: " + str(out1) + " Validation: " + str(out2)+"\n", flush=True)
        i+=1




    with open(folder + "MINI_other_GAUSS_newest", 'wb') as file:
        pickle.dump([output], file)

if method=='laplacian':
    folder=folder+"laplace/"
    output=[]
    prev=100
    sigma=1
    inistep=5
    precision=0.00001
    i=0
    steps=0
    maxstep=250
    diff=100
    while(abs(diff)>precision and steps<maxstep):
        GoodDir=True
        div=2**i
        step=inistep/div
        while (GoodDir):
            steps+=1
            sigma=sigma+step*(-1)**i
            KRR=KernelRidgeRegression(type="laplace")
            KRR.set_var(sigma=sigma, lambd=0.01)
            KRR.fit(X,Y,"error")
            out1=KRR.rmse
            KRR.predict(Xv,Yv)
            out2=KRR.rmse
            diff=prev-out1
            if diff<0:
                GoodDir=False
            prev=out1
            output.append([sigma,out1,out2])
            print("\nSigma: " + str(sigma) + " Train: " + str(out1) + " Validation: " + str(out2)+"\n", flush=True)
        i+=1


    with open(folder + "MINI_other_LAPLACE_newest", 'wb') as file:
        pickle.dump([output], file)
