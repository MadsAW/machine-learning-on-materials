#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 14:38:12 2018

@author: Simon
"""



from createLargerFeatureMatrix import simpleLargeMatrix
import pickle
import numpy as np

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




#%% Dummy data
X=np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15]])
Y=np.array(X.sum(axis=1))
X_v=(X+1)[:-1]
Y_v=(Y+3)[:-1]




#%% Define kernels

#A_3D kunne nok også have været A[:, np.newaxis, :]
#Dette er ikke en kernel. Funktionen bruges i guassian og laplacian
import numexpr as ne
def subt(A,B):
    A_3D = A[:, np.newaxis]
    return ne.evaluate('A_3D - B')


#Linar
def lin(A, B, c):
    return np.tensordot(A,B,axes=([1],[1]))+c

#Polynomial
def pol(A, B, c1, c2, d):
    return np.power(c1*np.tensordot(A,B,axes=([1],[1]))+c2,d)

#Gaussian
def gauss(A, B, sigma):
    return np.exp(   -np.square(np.linalg.norm(subt(A,B), axis=2)) / (2*(sigma**2))    )

#Laplacian
def laplace(A, B, sigma):
    return np.exp(   -(np.linalg.norm(subt(A,B), axis=2)) /  sigma    )








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


c=1
K=lin(X,X,c)
KAP_train=K
KAP_val=lin(X_v,X,c)

lam = 1
I = np.identity(len(X))


Y_predict_train = KAP_train @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
rmse_train = np.sqrt(np.mean(np.square(Y_predict_train-Y)))

Y_predict_val = KAP_val @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
rmse_val = np.sqrt(np.mean(np.square(Y_predict_val-Y_v)))

print(rmse_train)
print(rmse_val)





c1=1
c2=2
d=3
K=pol(X,X,c1,c2,d)
KAP_train=K
KAP_val=pol(X_v,X,c1,c2,d)

lam = 1
I = np.identity(len(X))


Y_predict_train = KAP_train @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
rmse_train = np.sqrt(np.mean(np.square(Y_predict_train-Y)))

Y_predict_val = KAP_val @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
rmse_val = np.sqrt(np.mean(np.square(Y_predict_val-Y_v)))

print(rmse_train)
print(rmse_val)






sigma=3
K=gauss(X,X,sigma)
KAP_train=K
KAP_val=gauss(X_v,X,sigma)

lam = 1
I = np.identity(len(X))


Y_predict_train = KAP_train @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
rmse_train = np.sqrt(np.mean(np.square(Y_predict_train-Y)))

Y_predict_val = KAP_val @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
rmse_val = np.sqrt(np.mean(np.square(Y_predict_val-Y_v)))

print(rmse_train)
print(rmse_val)








sigma=3
K=laplace(X,X,sigma)
KAP_train=K
KAP_val=laplace(X_v,X,sigma)



lam = 1
I = np.identity(len(X))


Y_predict_train = KAP_train @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
rmse_train = np.sqrt(np.mean(np.square(Y_predict_train-Y)))

Y_predict_val = KAP_val @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
rmse_val = np.sqrt(np.mean(np.square(Y_predict_val-Y_v)))

print(rmse_train)
print(rmse_val)










