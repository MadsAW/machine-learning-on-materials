
from createLargerFeatureMatrix import simpleLargeMatrix
import pickle
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import Flatten
from keras import backend
import numpy as np
import os







path = "Saved matrices/11-10-2018 11.36/sorted_Cutoff25_noSingleElementKrystals/"
featureMatrixFile = "test_featureMatrix.npy"
atomicSymbolsListFile = "test_pickledAtomicSymbolsList.txt"


largeFeatureMatrix, mappedAtomicNumber = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)


with open(path+"test_pickledEnergies.txt", "rb") as pickleFile:
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



#Compile model
model.compile(loss='mse', optimizer='adam', metrics=["mse"])

print(model.summary())


model_path='test4weights'


model.load_weights(model_path)


predictions = model.predict(X)


a=0
for i in range(len(predictions)):
    a+=(energies[i]-predictions[i])**2
rmse=np.sqrt(a/len(energies))
print(rmse)
