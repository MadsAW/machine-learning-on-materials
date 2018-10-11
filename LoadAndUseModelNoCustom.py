from keras.models import load_model
from keras import backend
import pickle
from createLargerFeatureMatrix import simpleLargeMatrix
import numpy as np




path = "Saved matrices/11-10-2018 11.36/sorted_Cutoff25_noSingleElementKrystals/"
featureMatrixFile = "featureMatrix.npy"
atomicSymbolsListFile = "pickledAtomicSymbolsList.txt"


largeFeatureMatrix, mappedAtomicNumber = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)
with open(path+"pickledEnergies.txt", "rb") as pickleFile:
    energies = pickle.load(pickleFile)

X = largeFeatureMatrix
Y = np.array(energies)


model_path='test4_model.h5'

model = load_model(model_path)

predictions = model.predict(X)

#Save weights
a=0
for i in range(len(predictions)):
    a+=(energies[i]-predictions[i])**2
rmse=np.sqrt(a/len(energies))
print(rmse)
