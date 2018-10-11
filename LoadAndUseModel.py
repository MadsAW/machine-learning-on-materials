from keras.models import load_model
from keras import backend
import pickle
from createLargerFeatureMatrix import simpleLargeMatrix
import numpy as np
from keras.utils import CustomObjectScope



path = "Saved matrices/26-09-2018 15.23/sorted_Cutoff25_noSingleElementKrystals/"
featureMatrixFile = "featureMatrix.npy"
atomicSymbolsListFile = "pickledAtomicSymbolsList.txt"


largeFeatureMatrix, mappedAtomicNumber = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)
with open(path+"pickledEnergies.txt", "rb") as pickleFile:
    energies = pickle.load(pickleFile)

X = largeFeatureMatrix
Y = np.array(energies)

#model = Sequential()
def rmse(y_true, y_pred):
	return backend.sqrt(backend.mean(backend.square(y_pred - y_true), axis=-1))


model_path=path+'test2_model.h5'

with CustomObjectScope({'rmse': rmse}):
    model = load_model(model_path)

predictions = model.predict(X)

#Save weights
a=0
for i in range(len(predictions)):
    a+=(energies[i]-predictions[i])**2
rmse=np.sqrt(a/len(energies))
print(rmse)
