
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 13:54:00 2018

@author: Simon
"""


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




#Dummy data
X=np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15]])
Y=np.array(X.sum(axis=1))
X_v=(X+1)[:-1]
Y_v=(Y+3)[:-1]



lam = 1
I = np.identity(len(X))


#Lineær
c=5
def f(xi,xj):
    return ((xi @ xj)+c)

K = np.zeros(I.shape)
for i in range(0,len(K)):
    for j in range(0,len(K)):
        K[i,j] = f(X[i],X[j])

#ovenstående loop er det samme som
K=np.tensordot(X,X,axes=([1],[1]))+c



#Polynomial
c1=1
c2=2
d=3
K=np.power(c1*np.tensordot(X,X,axes=([1],[1]))+c2,d)
def f(xi,xj):
    return (c1* (xi@xj) +c2)**d

#Gaussian
sigma=3



#Laplacian
sigma=3




KAP=[]
for i in range(len(X)):
    x=X[i]
    kap = np.zeros(len(X))
    for j in range(len(X)):
        kap[j] = f(X[j],x)
    KAP.append(kap)
KAP=np.array(KAP)

#For træningsdataen er kappa (som matrix) den samme som K. Ovenstående loop erstattes af
KAP_train=K

















XX=[]
for i in range(len(X_v)):
    x=X_v[i]
    kap = np.zeros(len(X))
    for j in range(len(X)):
        kap[j] = f(X[j],x)
    XX.append(kap)

XX=np.array(XX)

#Også for valideringen er kan kappa skrives på samme måde som K, 
#men her er første matrix nedenfor den fra valideringssættet. 
#Ovenstående loop er nedenstående er det samme
KAP_val=np.tensordot(X_v,X,axes=([1],[1]))+c





Y_predict_train = KAP_train @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
rmse_train = np.sqrt(np.mean(np.square(Y_predict_train-Y)))

Y_predict_val = KAP_val @ np.linalg.inv(np.matrix(K+lam*I)) @ Y
rmse_val = np.sqrt(np.mean(np.square(Y_predict_val-Y_v)))





print(rmse_train)

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

print(rmse_train)


print(rmse_val)




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

print(rmse_val)








