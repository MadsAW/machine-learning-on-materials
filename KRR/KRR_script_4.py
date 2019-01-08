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




if len(sys.argv)!=2:
    print('Usage: \n"python3 KRR_script.py method"\nwhere method is one of linear polynomial gaussian laplacian')
    sys.exit(1)

method=sys.argv[1]
lambd=float(sys.argv[2])
Feature=str(sys.argv[3])



path = "Saved matrices/03-01-2019 11.04/sorted_Cutoff25_noSingleElementKrystals/"
#%% Load training data
featureMatrixFile = "train_featureMatrix.npy"
atomicSymbolsListFile = "train_pickledAtomicSymbolsList.txt"
energiesFile = "train_pickledEnergies.txt"

if Feature="SimpleLarge":
    largeFeatureMatrix = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)
    folder=folder+"SimpleLarge/"
elif Feature="GP":
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
if Feature="SimpleLarge":
    largeFeatureMatrixValidate = simpleLargeMatrix(path,featureMatrixFileValidate, atomicSymbolsListFileValidate)
elif Feature="GP":
    largeFeatureMatrixValidate = advanced_large_matrix(path,featureMatrixFileValidate, atomicSymbolsListFileValidate)

with open(path+energiesFileValidate, "rb") as pickleFile:
    energiesValidate = pickle.load(pickleFile)

largeFeatureMatrixValidate.shape = (largeFeatureMatrixValidate.shape[0], -1)

Xv = largeFeatureMatrixValidate
Yv = np.array(energiesValidate)




#Kernel matrices output folder
folder = "KRR/Saved/Run 4/"

c_list = [10**n for n in range(-9,9)]
x = [-10**n for n in range(-9,9)]
x.reverse()
c_list = x + c_list

if method=='linear':
    out1_matrix_lin = np.zeros((len(c_list)))
    out2_matrix_lin = np.zeros((len(c_list)))
    folder=folder+"lin/"
    for c in range(len(c_list)):
        KRR=KernelRidgeRegression(type="linear")
        KRR.set_var(c1=c_list[c], lambd=lambd)
        KRR.fit(X,Y, "error")
        out1=KRR.rmse
        KRR.predict(Xv,Yv)
        out2=KRR.rmse
        print("\nTrain: " + str(out1) + " Validation: " + str(out2)+"\n", flush=True)
        out1_matrix_lin[c]=out1
        out2_matrix_lin[c]=out2



    with open(folder + "3_lin_train_"+str(lambd), 'wb') as file:
        pickle.dump([lambd, c_list, out1_matrix_lin], file)
    with open(folder + "3_lin_val_"+str(lambd), 'wb') as file:
        pickle.dump([lambd, c_list, out2_matrix_lin], file)







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






sigma_list = [0.1,0.5,1,5,10,25,50,100]

if method=='gaussian':
    folder=folder+"gauss/"
    out1_matrix_gauss = np.zeros((len(sigma_list)))
    out2_matrix_gauss = np.zeros((len(sigma_list)))
    for s in range(len(sigma_list)):
        KRR=KernelRidgeRegression(type="gauss")
        KRR.set_var(sigma=sigma_list[s], lambd=lambd)
        KRR.fit(X,Y, "error")
        out1=KRR.rmse
        KRR.predict(Xv,Yv)
        out2=KRR.rmse
        print("\nTrain: " + str(out1) + " Validation: " + str(out2)+"\n", flush=True)
        out1_matrix_gauss[s]=out1
        out2_matrix_gauss[s]=out2


    with open(folder + "3_gauss_train_"+str(lambd), 'wb') as file:
        pickle.dump([lambd, sigma_list, out1_matrix_gauss], file)
    with open(folder + "3_gauss_val_"+str(lambd), 'wb') as file:
        pickle.dump([lambd, sigma_list, out2_matrix_gauss], file)

if method=='laplacian':
    folder=folder+"laplace/"
    out1_matrix_laplace = np.zeros((len(sigma_list)))
    out2_matrix_laplace = np.zeros((len(sigma_list)))
    for s in range(len(sigma_list)):
        for l in range(len(lam_list)):
            KRR=KernelRidgeRegression(type="laplace")
            KRR.set_var(sigma=sigma_list[s], lambd=lam_list[l])
            KRR.fit(X,Y, "error")
            out1=KRR.rmse
            KRR.predict(Xv,Yv)
            out2=KRR.rmse
            print("\nTrain: " + str(out1) + " Validation: " + str(out2)+"\n", flush=True)


            out1_matrix_laplace[s]=out1
            out2_matrix_laplace[s]=out2


    with open(folder + "3_laplace_train_"+str(lambd), 'wb') as file:
        pickle.dump([lambd, sigma_list, out1_matrix_laplace], file)
    with open(folder + "3_laplace_val_"+str(lambd), 'wb') as file:
        pickle.dump([lambd, sigma_list, out2_matrix_laplace], file)
