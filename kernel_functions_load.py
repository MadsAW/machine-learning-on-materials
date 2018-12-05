#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 16:19:33 2018

@author: Simon
"""


from createLargerFeatureMatrix import simpleLargeMatrix
import pickle
import numpy as np
#import time
import numexpr as ne
train_bool = True

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

#X=X[:100]
#Y=Y[:100]

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

#X_v=X_v[:20]
#Y_v=Y_v[:20]


#%% Dummy data
"""
X=np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15]])
Y=np.array(X.sum(axis=1))
X_v=(X+1)[:-1]
Y_v=(Y+3)[:-1]
"""



#%% Define kernels

#A_3D kunne nok også have været A[:, np.newaxis, :]
#Dette er ikke en kernel. Funktionen bruges i guassian og laplacian
def subt(A,B):
    A_3D = A[:, np.newaxis]
    return ne.evaluate('A_3D - B')



#Linear
def lin(A, B, param):
    # param = c
    return np.tensordot(A,B,axes=([1],[1]))+param

#Polynomial, c1 must be positive, d must be a positve integer
def pol(A, B, param):
    # param = (c1, c2, d)
    # np.power(c1*np.tensordot(A,B,axes=([1],[1]))+c2,d)
    return np.power(param[0]*np.tensordot(A,B,axes=([1],[1]))+param[1],param[2])

#Gaussian, sigma must be positive
def gauss(A, B, param):
    # param = sigma
    return np.exp(   -np.square(np.linalg.norm(subt(A,B), axis=2)) / (2*(param**2))    )

#Laplacian, sigma must be positive
def laplace(A, B, param):
    # param = sigma
    return np.exp(   -(np.linalg.norm(subt(A,B), axis=2)) /  param   )








"""
#Sammenlign. Gauss
sigma=3

K = np.zeros((len(X),len(X)))
for i in range(0,len(K)):
    for j in range(0,len(K)):
        K[i,j] = np.exp(   -(    ( (X[i]-X[j])@(X[i]-X[j]) )    )/(2*(sigma**2)) )
print(K-gauss(X,X,3))


#Sammenlign. Laplace
sigma=3

K = np.zeros((len(X),len(X)))
for i in range(0,len(K)):
    for j in range(0,len(K)):
        K[i,j] = np.exp(   -(    np.sqrt( (X[i]-X[j])@(X[i]-X[j]) )    )/sigma )
print(K-laplace(X,X,3))
"""


#%% 
"""
func=lin
c=2
param = (c)
lam=3
"""

def calc(func, param, lam, train_bool):
    K=func(X,X,param)
    KAP_train=K
    KAP_val=func(X_v,X,param)
    
    I = np.identity(len(X))
    
    Y_predict_train = KAP_train @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
    rmse_train = np.sqrt(np.mean(np.square(Y_predict_train-Y)))
    
    print(func.__name__)
    print("param:" + str(param))
    print("lambda:" + str(lam))
    print(f"rmse train {rmse_train}")
    
    if train_bool != True:
        Y_predict_val = KAP_val @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
        rmse_val = np.sqrt(np.mean(np.square(Y_predict_val-Y_v)))
        print(f"rmse validation {rmse_val}")
        return rmse_train, rmse_val

    return rmse_train, "training"
    
    

print(calc(gauss,1,1,False))



"""
start = time.time()
L=np.linalg.cholesky(np.matrix(K+lam*I))
Y_predict_val_c = KAP_val @ (np.linalg.inv(L).T @ np.linalg.inv(L)) @ Y
print(f"cholesky prediction time validation: {time.time()-start}")
rmse_val_c = np.sqrt(np.mean(np.square(Y_predict_val_c-Y_v)))
"""









