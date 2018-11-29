#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 12:50:17 2018

@author: Simon
"""


import os
from createLargerFeatureMatrix import simpleLargeMatrix
import pickle
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import regularizers
import numpy as np
import sys
import pickle


if len(sys.argv)!=5:
    print("Usage: script.py dropout N activation n_hidden_layers")
    sys.exit(1)



path = "Saved matrices/11-10-2018 11.36/sorted_Cutoff25_noSingleElementKrystals/"


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





#Model
drop=float(sys.argv[1])
N=int(sys.argv[2])
act=sys.argv[3]
n_hidden=int(sys.argv[4])

model = Sequential()
    
inputShape = np.shape(X)[1:]

#First hidden layer after input
model.add(Dropout(drop, input_shape=inputShape))
model.add(Dense(N, activation=act))
#Addition hidden layers after input
for n in range(n_hidden-1):
    model.add(Dropout(drop))
    model.add(Dense(N//(2**(n+1)), activation=act))
#Output layer
model.add(Dropout(drop))
model.add(Dense(1))



#Compile model
model.compile(loss='mse', optimizer='adam', metrics=["mse"])

print(model.summary())

#Fit the model. This is where the hard computing happens. 
#Number of epochs is number of iterations through dataset
#Batch size is number of iterations before weights are changed.
history=model.fit(X, Y, epochs=70, batch_size=50, validation_data=(X_v,Y_v))

with open(f"histories func of depth/hist_N_{N}_drop_{drop}_acti_{act}_nhidden_{n_hidden}", 'wb') as file:
    pickle.dump(5, file)
    #pickle.dump(history.history, file)
    


#Evaluate model efficiency
scores = model.evaluate(X, Y)
print("\n%s: %.2f eV" % (model.metrics_names[1], scores[1]))








#Make predictions on training set
predictions = model.predict(X)
a=0
for i in range(len(predictions)):
    a+=(energies[i]-predictions[i])**2
rmse=np.sqrt(a/len(energies))

print("RMSE on training data "+str(rmse))





#Make predictions on validation set
predictionsValidate = model.predict(X_v)
a=0
for i in range(len(predictionsValidate)):
    a+=(energiesValidate[i]-predictionsValidate[i])**2
rmseValidate=np.sqrt(a/len(energiesValidate))

print("RMSE on validation data "+str(rmseValidate))




outs = ["Activation = "+act,"Drop = " + str(drop),"N = " + str(N), "Number of hidden layers (width halves with every layer) = " + str(n_hidden),"RMSE on training data "+str(rmse),"RMSE on validation data "+str(rmseValidate)]
outfile="rmse_drop_N_act_nhidden.txt"
with open(outfile, "a+") as file:
    for line in outs:
        file.write(line)
        file.write("\n")
    file.write("\n")



print("DONE")
