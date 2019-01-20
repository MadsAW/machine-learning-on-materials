# Neural network
This folder contain all scripts used by the neural network. The below table will show the primary files of the project and a quick description of the folders:

|File|Function|
|------|--------|
|NN_script|This is the main script. It will be called like: "python NN_script.py dropout N activation n_hidden_layers saved_matrix_folder feature_matrix_shape". Here, all parameters of the NN can be changed.|
|NN_script_best|This is the NN using the best parameters that were found. No options should be used when calling the script.|
|NN_script_dataset_size|Same as NN_script_best, but it does take one option when calling the script: the fraction of the training data that should be used, i.e. 0.1,0.2,...,0.9,1.0. This is to check if the training data is large enough.|


|Folder|Function|
|------|--------|
|Saved|This folder has all the saved results from the scripts|
|Shellscripts|This folder contains shellscripts used to creates jobs on the clusters|
|Old scripts|This folder contains some of the previous scripts|
