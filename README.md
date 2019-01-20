# machine-learning-on-materials
This is project is meant for an implementation of machine learning into a material database. The goal is to be able to predict the properties of the materials.

---
## General flow of the projects

The project is structured around several files and matrices that are used before the actual Neural Network (NN) is implemented. As such the project is effectively divided up into the following bits:

### Preprocessing of data

Here is an overview of the general flow when preprocessing data

|File|Description| Output|
|----|------------------------------------|-------|
|createFeatureMatrix|This file creates the feature matrix. This is done using prdf using the variables rs dr and rmax. The featrue matrix, energy list and atomicsymbol list are then Pickled|featureMatrix.npy, pickledEnergies.txt and pickledAtomicSymbolsList.txt|
|sortFeatureMatrix|This file uses the extracted feature matrix which it sorts. It sorts using a cutoff amount (least amount of representation of a certain element). It also removes all single crystal structures and makes sure that the arrays only contain numbers. A folder is created with the specifications used for sorting in which the new matrix is placed. Lastly this file also creates the train matrix and test (validation).| FullSet_featureMatrix.npy, FullSet_pickledEnergies.txt, FullSet_pickledAtomicSymbolsList.txt, same as before but with the prename test_ and train_|
|naivePredictions|This file tries through the simple models to predict the heat of formation. This is used for comparison with the ML models |NONE|
|createLargerFeatureMatrix|This file serves as a helper file containing a function that will create an enormous matrix (if it were to be stored ~30 GB using the simple description), this matrix is the matrix that is fed to the ML models and is one of the feature matrices described by feature matrices. |NONE|
|test4|This file creates the NN and uses the featurematrix to train the ML models. When done it will save the weights|filename+"weights"|
|LoadAndUseModekNoCustom|This file loads the previous saved weights and the uses the NN on the matrix.|NONE|

## Connected folders

This will serve as a quick overview of the folders in the project:

|Folder|Function|
|------|--------|
|Output|This folder stores all output files created using gbar|
|NN|This folder contains all scripts related to the Neural Network|
|KRR|This folder contains all scripts related to the Kernel Ridge Regression|
|Saved matrices|This folder contains all the feature matrices we have created in a sorted and non-sorted version. Also present is a folder with the PRDF parameters that were used to create the matrix|
