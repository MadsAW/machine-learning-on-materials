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
from keras import backend
import numpy as np
import os


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






#Create model
model = Sequential()

inputShape = np.shape(X)[1:]

model.add(Dense(200, input_shape=inputShape, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(1))





"""
#Root mean squared error metric
def rmse(y_true, y_pred):
	return backend.sqrt(backend.mean(backend.square(y_pred - y_true), axis=-1))
"""


#Compile model
model.compile(loss='mse', optimizer='adam', metrics=["mse"])

print(model.summary())

#Fit the model. This is where the hard computing happens. 
#Number of epochs is number of iterations through dataset
#Batch size is number of iterations before weights are changed.
model.fit(X, Y, epochs=40, batch_size=50)

#Evaluate model efficiency
scores = model.evaluate(X, Y)
print("\n%s: %.2f eV" % (model.metrics_names[1], scores[1]))

#Make predictions
predictions = model.predict(X)

#Save weights
model.save_weights(os.path.basename(__file__)[:-3]+"weights")


a=0
for i in range(len(predictions)):
    a+=(energies[i]-predictions[i])**2
rmse=np.sqrt(a/len(energies))
