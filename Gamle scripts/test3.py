#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 10:51:19 2018

@author: Simon
"""


import pickle
from getGroupAndPeriod import getGroupAndPeriod
from keras.models import Sequential
from keras.layers import Dense
from keras import backend
import numpy as np


path = "Saved matrices/26-09-2018 15.23/sorted_Cutoff25_noSingleElementKrystals/"
featureMatrixFile = "featureMatrix.npy"



featureMatrix=np.load(path+featureMatrixFile)

with open(path+"pickledAtomicSymbolsList.txt", "rb") as pickleFile:
    atomicSymbolsList = pickle.load(pickleFile)

with open(path+"pickledEnergies.txt", "rb") as pickleFile:
    energies = pickle.load(pickleFile)

flatMatrix=np.reshape(featureMatrix,(np.shape(featureMatrix)[0],np.product(np.shape(featureMatrix)[1:])))

index=0
groups_periods=np.zeros((len(flatMatrix),4))
for i in atomicSymbolsList:
    groups_periods[index,0:2]=getGroupAndPeriod(i[0])
    groups_periods[index,2:]=getGroupAndPeriod(i[1])
    index+=1


X = np.hstack([groups_periods,flatMatrix])
Y = np.array(energies)






#Create model
model = Sequential()

inputShape = np.shape(X)[1:]

model.add(Dense(200, input_shape=inputShape, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(1, activation='relu'))
model.add(Dense(1))






#Root mean squared error metric
def rmse(y_true, y_pred):
	return backend.sqrt(backend.mean(backend.square(y_pred - y_true), axis=-1))



#Compile model
model.compile(loss='mean_squared_error', optimizer='adam', metrics=[rmse])






#Fit the model. This is where the hard computing happens. 
#Number of epochs is number of iterations through dataset
#Batch size is number of iterations before weights are changed.
model.fit(X, Y, epochs=5000, batch_size=10)




#Evaluate model efficiency
scores = model.evaluate(X, Y)
print("\n%s: %.2f eV" % (model.metrics_names[1], scores[1]))

#Make predictions
predictions = model.predict(X)

#Save weights
model.save(path+"test3_model.h5")


a=0
for i in range(len(predictions)):
    a+=(energies[i]-predictions[i])**2
rmse=np.sqrt(a/len(energies))