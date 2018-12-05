#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 14:40:54 2018

@author: Simon
"""

from createLargerFeatureMatrix import simpleLargeMatrix
from KRR_class import KernelRidgeRegression
import pickle
import numpy as np
import sys




if len(sys.argv)!=2:
    print('Usage: \n"python3 kernel_script_class.py method"\nwhere method is one of linear polynomial gaussian laplacian')
    sys.exit(1)

method=sys.argv[1]



path = "Saved matrices/11-10-2018 11.36/sorted_Cutoff25_noSingleElementKrystals/"
#%% Load training data
featureMatrixFile = "train_featureMatrix.npy"
atomicSymbolsListFile = "train_pickledAtomicSymbolsList.txt"
energiesFile = "train_pickledEnergies.txt"

largeFeatureMatrix, mappedAtomicNumber = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)


with open(path+energiesFile, "rb") as pickleFile:
    energies = pickle.load(pickleFile)

largeFeatureMatrix.shape = (largeFeatureMatrix.shape[0], -1)

X = largeFeatureMatrix
Y = np.array(energies)

#%% Load validation data
featureMatrixFileValidate = "validate_featureMatrix.npy"
atomicSymbolsListFileValidate = "validate_pickledAtomicSymbolsList.txt"
energiesFileValidate = "validate_pickledEnergies.txt"

largeFeatureMatrixValidate, mappedAtomicNumberValidate = simpleLargeMatrix(path,featureMatrixFileValidate, atomicSymbolsListFileValidate)


with open(path+energiesFileValidate, "rb") as pickleFile:
    energiesValidate = pickle.load(pickleFile)

largeFeatureMatrixValidate.shape = (largeFeatureMatrixValidate.shape[0], -1)

X_v = largeFeatureMatrixValidate
Y_v = np.array(energiesValidate)

#%%


#Define parameters
lam_list = [10**n for n in range(-2,5)]


c_list = [10**n for n in range(-2,5)]
x = [10**n for n in range(-2,5)]
x.reverse()
c_list = x + c_list


c1_list = [10**n for n in range(-2,2)]


c2_list = [10**n for n in range(-2,2)]
x = [10**n for n in range(-2,2)]
x.reverse()
c2_list = x + c2_list


d_list = [10**n for n in range(-2,2)]


sigma_list = [10**n for n in range(-2,2)]


#Kernel matrices output folder
folder = "kernel pickles/"

#%%
out=1

if method=='linear':
    out_matrix_lin = np.zeros((len(c_list), len(lam_list)))
    for c in range(len(c_list)):
        for l in range(len(lam_list)):
            print(f'c={c_list[c]}, lambda={lam_list[l]}')
            
            KRR=KernelRidgeRegression(type="linear")
            KRR.set_var(c1=c_list[c], lamd=lam_list[l])
            KRR.fit(X,Y)
            Y_predict_val=KRR.predict(X_v,Y_v)
            
            out=KRR.rmse
            print(out)
            
            out_matrix_lin[c,l]=out
    
    
    with open(folder + "out_matrix_lin", 'wb') as file:
        pickle.dump(out_matrix_lin, file)


elif method=='polynomial':
    out_matrix_pol = np.zeros((len(c1_list), len(c2_list), len(d_list), len(lam_list)))
    for c1 in range(len(c1_list)):
        for c2 in range(len(c2_list)):
            for d in range(len(d_list)):
                for l in range(len(lam_list)):
                    print(f'c1={c1_list[c1]}, c2={c2_list[c2]}, d={d_list[d]}, lambda={lam_list[l]}')
                    
                    KRR=KernelRidgeRegression(type="poly")
                    KRR.set_var(c1=c1_list[c1],c2=c2_list[c2],d=d_list[d], lamd=lam_list[l])
                    KRR.fit(X,Y)
                    Y_predict_val=KRR.predict(X_v,Y_v)
                    
                    out=KRR.rmse
                    print(out)
                    
                    out_matrix_pol[c1,c2,d,l]=out
            
    with open(folder + "out_matrix_pol", 'wb') as file:
        pickle.dump(out_matrix_pol, file)


    
elif method=='gaussian':
    out_matrix_gauss = np.zeros((len(sigma_list), len(lam_list)))
    for s in range(len(sigma_list)):
        for l in range(len(lam_list)):
            print(f'sigma={sigma_list[s]}, lambda={lam_list[l]}')
    
            KRR=KernelRidgeRegression(type="gauss")
            KRR.set_var(sigma=sigma_list[s], lamd=lam_list[l])
            KRR.fit(X,Y)
            Y_predict_val=KRR.predict(X_v,Y_v)
            
            out=KRR.rmse
            print(out)
    
    
            out_matrix_gauss[s,l]=out
    
    
    with open(folder + "out_matrix_gauss", 'wb') as file:
        pickle.dump(out_matrix_gauss, file)




elif method=='laplacian':
    out_matrix_laplace = np.zeros((len(sigma_list), len(lam_list)))
    for s in range(len(sigma_list)):
        for l in range(len(lam_list)):
            print(f'sigma={sigma_list[s]}, lambda={lam_list[l]}')
    
            KRR=KernelRidgeRegression(type="laplace")
            KRR.set_var(sigma=sigma_list[s], lamd=lam_list[l])
            KRR.fit(X,Y)
            Y_predict_val=KRR.predict(X_v,Y_v)
            
            out=KRR.rmse
            print(out)
    
    
            out_matrix_laplace[s,l]=out   
            
    
    with open(folder + "out_matrix_laplace", 'wb') as file:
        pickle.dump(out_matrix_laplace, file)