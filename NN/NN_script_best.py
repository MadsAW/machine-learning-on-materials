#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 12:50:17 2018

@author: Simon
"""


import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if os.getcwd()[-2:] == 'NN':
    os.chdir('..')

from createLargerFeatureMatrix import simpleLargeMatrix, no_redundancy_matrix, advanced_large_matrix
import pickle
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import regularizers
import numpy as np





drop=0.3
N=350
act="sigmoid"
n_hidden=1
saved_matrix_folder="03-01-2019 11.04"
feature_matrix_shape="group_period_x_group_period"

for i in range(5):
    for act in ['sigmoid','relu']:
        
        matrix_functions={"atomic_number":simpleLargeMatrix, "group_period_2x2":no_redundancy_matrix, "group_period_x_group_period":advanced_large_matrix}
        matrix_function=matrix_functions[feature_matrix_shape]
        path = "Saved matrices/"+saved_matrix_folder+"/sorted_Cutoff25_noSingleElementKrystals/"
        histories_folder='best'
        
        if histories_folder not in os.listdir("NN/Saved"):
            os.mkdir("NN/Saved/"+histories_folder)
        
        #Load training data
        featureMatrixFile = "train_featureMatrix.npy"
        atomicSymbolsListFile = "train_pickledAtomicSymbolsList.txt"
        energiesFile = "train_pickledEnergies.txt"
        
        largeFeatureMatrix = matrix_function(path,featureMatrixFile, atomicSymbolsListFile)
        
        with open(path+energiesFile, "rb") as pickleFile:
            energies = pickle.load(pickleFile)
        
        print(largeFeatureMatrix.shape)
        largeFeatureMatrix.shape = (largeFeatureMatrix.shape[0], -1)
        
        X = largeFeatureMatrix
        Y = np.array(energies)
        
        
        
        #Load validation set
        featureMatrixFileValidate = "validate_featureMatrix.npy"
        atomicSymbolsListFileValidate = "validate_pickledAtomicSymbolsList.txt"
        energiesFileValidate = "validate_pickledEnergies.txt"
        
        
        largeFeatureMatrixValidate = matrix_function(path,featureMatrixFileValidate, atomicSymbolsListFileValidate)
        
        
        
        with open(path+energiesFileValidate, "rb") as pickleFile:
            energiesValidate = pickle.load(pickleFile)
        
        largeFeatureMatrixValidate.shape = (largeFeatureMatrixValidate.shape[0], -1)
        
        X_v = largeFeatureMatrixValidate
        Y_v = np.array(energiesValidate)
        
        
        
        
        #Load test set
        featureMatrixFileTest = "test_featureMatrix.npy"
        atomicSymbolsListFileTest = "test_pickledAtomicSymbolsList.txt"
        energiesFileTest = "test_pickledEnergies.txt"
        
        
        largeFeatureMatrixTest = matrix_function(path,featureMatrixFileTest, atomicSymbolsListFileTest)
        
        
        
        with open(path+energiesFileTest, "rb") as pickleFile:
            energiesTest = pickle.load(pickleFile)
        
        largeFeatureMatrixTest.shape = (largeFeatureMatrixTest.shape[0], -1)
        
        X_t = largeFeatureMatrixTest
        Y_t = np.array(energiesTest)
        
        
        
        
        #Model
        
        model = Sequential()
        
        inputShape = np.shape(X)[1:]
        
        #First hidden layer after input
        model.add(Dropout(drop, input_shape=inputShape))
        model.add(Dense(N, activation=act))
        #Addition hidden layers after input
        for n in range(n_hidden-1):
            model.add(Dropout(drop))
            model.add(Dense(N//(2**(n+1)), activation=act))
        #Output layer
        model.add(Dropout(drop))
        model.add(Dense(1))
        
        
        
        #Compile model
        model.compile(loss='mse', optimizer='adam', metrics=["mse"])
        
        print(model.summary())
        
        #Fit the model. This is where the hard computing happens.
        #Number of epochs is number of iterations through dataset
        #Batch size is number of iterations before weights are changed.
        history=model.fit(X, Y, epochs=70, batch_size=50, validation_data=(X_v,Y_v))
        
        best_saved=os.listdir("NN/Saved/"+histories_folder)
        
        file_num=1
        num_found=False
        while num_found == False:
            if f"history{file_num}{act}" in best_saved:
                file_num+=1
            else:
                num_found = True
        
        with open(f"NN/Saved/"+histories_folder+f"/history"+str(file_num)+act, 'wb') as file:
            pickle.dump(history.history, file)
        
#        with open(f"NN/Saved/"+histories_folder+f"/model"+str(file_num), 'wb') as file:
#            pickle.dump(model, file)
        
        model.save(f"NN/Saved/"+histories_folder+f"/model"+str(file_num)+act+'.h5')
        
        
        
        #Evaluate model efficiency
        #scores = model.evaluate(X, Y)
        #print("\n%s: %.2f eV" % (model.metrics_names[1], scores[1]))
        
        
        
        #Make predictions on training set
        predictions = model.predict(X)
        a=0
        for i in range(len(predictions)):
            a+=(energies[i]-predictions[i])**2
        rmse=np.sqrt(a/len(energies))
        
        print("RMSE on training data "+str(rmse))
        
        
        
        
        
        #Make predictions on validation set
        predictions_validate = model.predict(X_v)
        a=0
        for i in range(len(predictions_validate)):
            a+=(energiesValidate[i]-predictions_validate[i])**2
        rmseValidate=np.sqrt(a/len(energiesValidate))
        
        print("RMSE on validation data "+str(rmseValidate))
        
        
        #Make predictions on test set
        predictions_test = model.predict(X_t)
        a=0
        for i in range(len(predictions_test)):
            a+=(energiesTest[i]-predictions_test[i])**2
        rmseTest=np.sqrt(a/len(energiesTest))
        
        print("RMSE on test data "+str(rmseTest))
        
        
        
        
        
        first_outs=["Activation = "+act,"Drop = " + str(drop),"N = " + str(N), "Number of hidden layers (width halves with every layer) = " + str(n_hidden), "Saved matrix folder = "+saved_matrix_folder,"Matrix shape = "+feature_matrix_shape]
        outs = ["Activation: "+act, "Model number= = "+str(file_num),"RMSE on training data= "+str(rmse),"RMSE on validation data= "+str(rmseValidate),"RMSE on test data= "+str(rmseTest)]
        
        outfile="NN/Saved/best/best_outputs.txt"
        with open(outfile, "a+") as file:
            if "best_outputs.txt" not in best_saved:
                for line in first_outs[1:]:
                    file.write(line)
                    file.write("\n")
            for line in outs:
                file.write(line)
                file.write("\n")
            file.write("\n")
        
        
        
        print("DONE")
