#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 12:50:17 2018

Trains the NN with the parameters:
dropout=0.3
Size of first hidden lauer: 350
One hidden layers
Sigmoid Activation
Using matrix from folder: 03-01-2019 11.04
Using GP matrix shape

One option should be used when calling the script:
The fraction of the training data that should be used when training the NN.
"""


import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if os.getcwd()[-2:] == 'NN':
    os.chdir('..')

from createLargerFeatureMatrix import simpleLargeMatrix, no_redundancy_matrix, advanced_large_matrix
import pickle
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import regularizers
import numpy as np


pct=float(sys.argv[1])



drop=0.3
N=350
act="sigmoid"
n_hidden=1
saved_matrix_folder="03-01-2019 11.04"
feature_matrix_shape="group_period_x_group_period"


matrix_functions={"atomic_number":simpleLargeMatrix, "group_period_2x2":no_redundancy_matrix, "group_period_x_group_period":advanced_large_matrix}
matrix_function=matrix_functions[feature_matrix_shape]
path = "Saved matrices/"+saved_matrix_folder+"/sorted_Cutoff25_noSingleElementKrystals/"
histories_folder='data_size'

if histories_folder not in os.listdir("NN/Saved"):
    os.mkdir("NN/Saved/"+histories_folder)

#Load training data
featureMatrixFile = "train_featureMatrix.npy"
atomicSymbolsListFile = "train_pickledAtomicSymbolsList.txt"
energiesFile = "train_pickledEnergies.txt"

largeFeatureMatrix = matrix_function(path,featureMatrixFile, atomicSymbolsListFile)

with open(path+energiesFile, "rb") as pickleFile:
    energies = pickle.load(pickleFile)

print(largeFeatureMatrix.shape)
largeFeatureMatrix.shape = (largeFeatureMatrix.shape[0], -1)

X = largeFeatureMatrix[0:int(len(largeFeatureMatrix)*pct),:]
Y = np.array(energies)[0:int(len(largeFeatureMatrix)*pct)]



#Load validation set
featureMatrixFileValidate = "validate_featureMatrix.npy"
atomicSymbolsListFileValidate = "validate_pickledAtomicSymbolsList.txt"
energiesFileValidate = "validate_pickledEnergies.txt"


largeFeatureMatrixValidate = matrix_function(path,featureMatrixFileValidate, atomicSymbolsListFileValidate)



with open(path+energiesFileValidate, "rb") as pickleFile:
    energiesValidate = pickle.load(pickleFile)

largeFeatureMatrixValidate.shape = (largeFeatureMatrixValidate.shape[0], -1)

X_v = largeFeatureMatrixValidate
Y_v = np.array(energiesValidate)






#Model

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

best_saved=os.listdir("NN/Saved/"+histories_folder)

file_num=1
num_found=False
while num_found == False:
    if f"history{file_num}" in best_saved:
        file_num+=1
    else:
        num_found = True

with open(f"NN/Saved/"+histories_folder+f"/history"+str(file_num), 'wb') as file:
    pickle.dump([pct, history.history], file)



print("DONE")
