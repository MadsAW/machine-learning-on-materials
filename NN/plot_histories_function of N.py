#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 11:49:16 2018

@author: Simon
"""

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

os.chdir("Saved/histories func of N")

files = [file for file in os.listdir() if file!='plots' and file!='.DS_Store']
data={"relu":{0.4:[[],[],[]], 0.7:[[],[],[]]},"sigmoid":{0.4:[[],[],[]], 0.7:[[],[],[]]}}

for file in files:
    with open(file, "rb") as pickleFile:
        history = pickle.load(pickleFile)

    rmse_train_list = [elem**(1/2) for elem in history['mean_squared_error']]
    rmse_val_list = [elem**(1/2) for elem in history['val_mean_squared_error']]

    rmse_train = np.mean(rmse_train_list[-10:])
    rmse_val = np.mean(rmse_val_list[-10:])

    N=int(file[7:file.find("_",7)])
    drop=float(file[file.find("drop")+5:file.find("_",file.find("drop")+5)])
    act=file[file.find("acti")+5:]

    data[act][drop][0].append(N)
    data[act][drop][1].append(rmse_train)
    data[act][drop][2].append(rmse_val)

relu_04=np.array(data["relu"][0.4])
relu_04=relu_04[:,np.argsort(relu_04[0])].tolist()

relu_07=np.array(data["relu"][0.7])
relu_07=relu_07[:,np.argsort(relu_07[0])].tolist()

sigmoid_04=np.array(data["sigmoid"][0.4])
sigmoid_04=sigmoid_04[:,np.argsort(sigmoid_04[0])].tolist()

sigmoid_07=np.array(data["sigmoid"][0.7])
sigmoid_07=sigmoid_07[:,np.argsort(sigmoid_07[0])].tolist()


data_list=[relu_04,relu_07,sigmoid_04,sigmoid_07]
title_list=['Relu, dropout 40%','Relu, dropout 70%','Sigmoid, dropout 40%','Sigmoid, dropout 70%']
name_list=['Relu_drop_0.4','Relu_drop_0.7','Sigmoid_drop_0.4','Sigmoid_drop_0.7']

for i in range(len(data_list)):
    plt.plot(data_list[i][0],data_list[i][1], 'b', label='train')
    plt.plot(data_list[i][0],data_list[i][2], 'r', label='validation')
    plt.legend()
    plt.title(title_list[i])
    plt.xlabel('N')
    plt.ylabel('Root mean squared error')
    plt.ylim(0.1,0.6)

    plt.savefig(f'plots/'+name_list[i]+'.png')
    plt.show()
