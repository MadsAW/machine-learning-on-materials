
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 13:54:00 2018

@author: Simon
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from createLargerFeatureMatrix import simpleLargeMatrix
import pickle
import numpy as np

path = "Saved matrices/11-10-2018 11.36/sorted_Cutoff25_noSingleElementKrystals/"
#%%
#Load training data
featureMatrixFile = "train_featureMatrix.npy"
atomicSymbolsListFile = "train_pickledAtomicSymbolsList.txt"
energiesFile = "train_pickledEnergies.txt"

largeFeatureMatrix, mappedAtomicNumber = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)


with open(path+energiesFile, "rb") as pickleFile:
    energies = pickle.load(pickleFile)

largeFeatureMatrix.shape = (largeFeatureMatrix.shape[0], -1)

X = largeFeatureMatrix
Y = np.array(energies)



#%%
#Load validation data
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
#Dummy data
X=np.reshape(np.arange(15),(5,3))
Y=np.array(X.sum(axis=1))
X_v=(X+7)[:-1]
Y_v=(Y+7*3)[:-1]


#%%
class KRR:

    def __init__(self):
        self.available_kernels = ['linear','pol','gauss','laplace']
        self.kernel_type = None
        self.K = None
        self.lam = None


    def set_kernel_type(self, arg):
        if arg not in self.available_kernels:
            print(f'Usage: KRR.set_kernel_type(arg) where arg is one of {self.available_kernels}. Kernel not set.')
            raise Exception('Invalid kernel')
        else:
            self.kernel_type=arg


    def set_lam(self,lam):
        if type(lam) != int and type(lam) != float:
            print('Lambda must be a number')
            raise Exception('Not a number')
        else:
            self.lam = lam





k=KRR()
print(k.available_kernels)
k.set_kernel_type('linear')
print(k.kernel_type)
k.set_lam(2.1)
print(k.lam)




#%%
"""
lam = 1
I = np.identity(len(X))

c=1
def f(xi,xj):
    return (xi @ xj)+c

K = np.zeros(I.shape)
for i in range(0,len(K)):
    for j in range(0,len(K)):
        K[i,j] = f(X[i],X[j])




diff=[]

for i in range(len(X)):
    x=X[i]
    kap = np.zeros(len(X))
    for j in range(len(X)):
        kap[j] = f(X[j],x)

    y=(kap @ np.linalg.inv(np.matrix(K+lam*I)) @ Y)

    diff.append((Y[i]-y)[0,0])




#rmse on training
rmse_train = np.sqrt(np.mean(np.square(diff)))








#Make predictions on validation set
diff=[]

for i in range(len(X_v)):
    x=X_v[i]
    kap = np.zeros(len(X))
    for j in range(len(X)):
        kap[j] = f(X[j],x)

    y=(kap @ np.linalg.inv(np.matrix(K+lam*I)) @ Y)

    diff.append((Y_v[i]-y)[0,0])




#rmse on training
rmse_val = np.sqrt(np.mean(np.square(diff)))




print("RMSE on training data "+str(rmse_train))
print("RMSE on validation data "+str(rmse_val))







print("DONE")
"""
