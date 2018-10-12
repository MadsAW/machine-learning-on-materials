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
