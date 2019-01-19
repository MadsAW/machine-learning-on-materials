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
