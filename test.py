#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 11:57:35 2018

@author: Simon
"""

from createLargerFeatureMatrix import simpleLargeMatrix
import pickle
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
import numpy as np


path = "Saved matrices/24-09-2018 21.44/sorted_Cutoff25_noSingleElementKrystals/"
featureMatrixFile = "featureMatrix.npy"
atomicSymbolsListFile = "pickledAtomicSymbolsList.txt"


largeFeatureMatrix, mappedAtomicNumber = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)


with open(path+"pickledEnergies.txt", "rb") as pickleFile:
    energies = pickle.load(pickleFile)


X = largeFeatureMatrix
Y = np.array(energies)






#Create model
model = Sequential()
inputShape = np.shape(X)[1:]
outputShape = np.shape(Y)[1:]

model.add(Dense(800, input_shape=inputShape, activation='relu'))
model.add(Dense(400, activation='relu'))
model.add(Flatten(input_shape=inputShape))
model.add(Dense(1 , activation='relu'))
#model.add(Dense(1, output_shape=outputShape , activation='relu'))

#Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Fit the model. This is where the hard computing happens. 
#Number of epochs is number of iterations through dataset
#Batch size is number of iterations before weights are changed.
model.fit(X, Y, epochs=150, batch_size=10)

#Evaluate model efficiency
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

#Make predictions
predictions = model.predict(X)
