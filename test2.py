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


path = "Saved matrices/26-09-2018 15.23/sorted_Cutoff25_noSingleElementKrystals/"
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

model.add(Dense(196, input_shape=inputShape, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(1, activation='relu'))
model.add(Flatten())
model.add(Dense(1))






#Root mean squared error metric
def rmse(y_true, y_pred):
	return backend.sqrt(backend.mean(backend.square(y_pred - y_true), axis=-1))



#Compile model
model.compile(loss='mean_squared_error', optimizer='adam', metrics=[rmse])




#Fit the model. This is where the hard computing happens. 
#Number of epochs is number of iterations through dataset
#Batch size is number of iterations before weights are changed.
model.fit(X, Y, epochs=16, batch_size=10)

#Evaluate model efficiency
scores = model.evaluate(X, Y)
print("\n%s: %.2f eV" % (model.metrics_names[1], scores[1]))

#Make predictions
predictions = model.predict(X)

#Save weights
model.save(path+"test2_model.h5")


a=0
for i in range(len(predictions)):
    a+=(energies[i]-predictions[i])**2
rmse=np.sqrt(a/len(energies))