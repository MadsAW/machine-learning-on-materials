from keras.models import load_model
from keras import backend
import pickle
from createLargerFeatureMatrix import simpleLargeMatrix
import numpy as np
from keras.utils import CustomObjectScope


#Define path to model that we want to load
path = "Saved matrices/26-09-2018 15.23/sorted_Cutoff25_noSingleElementKrystals/"
#Define the matrix files
featureMatrixFile = "featureMatrix.npy"
atomicSymbolsListFile = "pickledAtomicSymbolsList.txt"

#Create feature matrix in RAM
largeFeatureMatrix, mappedAtomicNumber = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)
with open(path+"pickledEnergies.txt", "rb") as pickleFile:
    energies = pickle.load(pickleFile)

X = largeFeatureMatrix
Y = np.array(energies)

#Define custom method used in model
def rmse(y_true, y_pred):
	return backend.sqrt(backend.mean(backend.square(y_pred - y_true), axis=-1))

<<<<<<< HEAD:LoadAndUseModel.py
#Load model
=======

>>>>>>> 28ba819a50312b5b4bd37d4ccb110cad9c30a1b6:Gamle scripts/LoadAndUseModel.py
model_path=path+'test2_model.h5'

with CustomObjectScope({'rmse': rmse}):
    model = load_model(model_path)

#predict
predictions = model.predict(X[0:10])

#Judge how good the prediction is
a=0
for i in range(len(predictions)):
    a+=(energies[i]-predictions[i])**2
rmse=np.sqrt(a/len(energies))
print(rmse)
