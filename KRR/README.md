# Kernel Ridge Regression
This folder contain all scripts used by the kernel ridge regression. The below table will show the primary files of the project and a quick description of the folders:

|File|Function|
|------|--------|
|KRR_class|This file contains the Kernel Ridge Regression class used to create the KRR models.|
|minimmizer|This file is made so that it can be initialized from the command line and then uses Nelder-Mead minimization to find a local minima|
|KRR_scriptXXX|These scripts were used to obtain several datapoinnts, they are however quite slow since each needs a lot of calculations as such they have been replaced by the file batch_KRR|
|batch_KRR|This file utilizes the structure of the hpc cluster and only does one calculation according to the arguments passed in command line. This is used in combination with writeshells to create the shellscripts each a job doing 1 calculation.|
|writeshells|Writeshells create the shellscripts for a certain python script to obtain several datapoints.|

|Folder|Function|
|------|--------|
|Saved|This folder has all the saved results from the shellscripts, these include datapoints for the various parameters|
|Shellscripts|This folder contains shellscripts used to creates jobs on the clusters|
|Unused scripts|This folder contains some of the previous scripts|

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
