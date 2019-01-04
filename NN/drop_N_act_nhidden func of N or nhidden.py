#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 13:18:03 2018

@author: Simon
"""


import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pickle
import numpy as np
import matplotlib.pyplot as plt

os.chdir("histories func of depth")

files = [file for file in os.listdir() if file!='plots' and file!='.DS_Store']
data={"relu":{0.3:{25:[[],[],[]], 250:[[],[],[]], 1000:[[],[],[]]}, 0.5:{25:[[],[],[]], 250:[[],[],[]], 1000:[[],[],[]]}},"sigmoid":{0.3:{25:[[],[],[]], 250:[[],[],[]], 1000:[[],[],[]]}, 0.5:{25:[[],[],[]], 250:[[],[],[]], 1000:[[],[],[]]}}}

for file in files:
    with open(file, "rb") as pickleFile:
        history = pickle.load(pickleFile)

    rmse_train_list = [elem**(1/2) for elem in history['mean_squared_error']]
    rmse_val_list = [elem**(1/2) for elem in history['val_mean_squared_error']]

    rmse_train = np.mean(rmse_train_list[-10:])
    rmse_val = np.mean(rmse_val_list[-10:])

    N=int(file[7:file.find("_",7)])
    drop=float(file[file.find("drop")+5:file.find("_",file.find("drop")+5)])
    act=file[file.find("acti")+5:file.find("_",file.find("acti")+5)]
    n_hidden=file[file.find("nhidden")+8:]

    data[act][drop][N][0].append(n_hidden)
    data[act][drop][N][1].append(rmse_train)
    data[act][drop][N][2].append(rmse_val)

#25
relu_03_25=np.array(data["relu"][0.3])
relu_03_25=relu_03_25[:,np.argsort(relu_03_25[0])].tolist()

relu_05_25=np.array(data["relu"][0.5])
relu_05_25=relu_05_25[:,np.argsort(relu_05_25[0])].tolist()

sigmoid_03_25=np.array(data["sigmoid"][0.4])
sigmoid_03_25=sigmoid_03_25[:,np.argsort(sigmoid_03_25[0])].tolist()

sigmoid_05_25=np.array(data["sigmoid"][0.7])
sigmoid_05_25=sigmoid_05_25[:,np.argsort(sigmoid_05_25[0])].tolist()

#250
relu_03_250=np.array(data["relu"][0.3])
relu_03_250=relu_03_250[:,np.argsort(relu_03_250[0])].tolist()

relu_05_250=np.array(data["relu"][0.5])
relu_05_250=relu_05_250[:,np.argsort(relu_05_250[0])].tolist()

sigmoid_03_250=np.array(data["sigmoid"][0.4])
sigmoid_03_250=sigmoid_03_250[:,np.argsort(sigmoid_03_250[0])].tolist()

sigmoid_05_250=np.array(data["sigmoid"][0.7])
sigmoid_05_250=sigmoid_05_250[:,np.argsort(sigmoid_05_250[0])].tolist()

#1000
relu_03_1000=np.array(data["relu"][0.3])
relu_03_1000=relu_03_1000[:,np.argsort(relu_03_1000[0])].tolist()

relu_05_1000=np.array(data["relu"][0.5])
relu_05_1000=relu_05_1000[:,np.argsort(relu_05_1000[0])].tolist()

sigmoid_03_1000=np.array(data["sigmoid"][0.4])
sigmoid_03_1000=sigmoid_03_1000[:,np.argsort(sigmoid_03_1000[0])].tolist()

sigmoid_05_1000=np.array(data["sigmoid"][0.7])
sigmoid_05_1000=sigmoid_05_1000[:,np.argsort(sigmoid_05_1000[0])].tolist()


data_list=[relu_03_25,relu_05_25,sigmoid_03_25,sigmoid_05_25,relu_03_250,relu_05_250,sigmoid_03_250,sigmoid_05_250,relu_03_1000,relu_05_1000,sigmoid_03_1000,sigmoid_05_1000]
title_list=['Relu, dropout 30pct, width of first hidden layer 25','Relu, dropout 50pct, width of first hidden layer 25','Sigmoid, dropout 30pct, width of first hidden layer 25','Sigmoid, dropout 50pct, width of first hidden layer 25','Relu, dropout 30pct, width of first hidden layer 250','Relu, dropout 50pct, width of first hidden layer 250','Sigmoid, dropout 30pct, width of first hidden layer 250','Sigmoid, dropout 50pct, width of first hidden layer 250','Relu, dropout 30pct, width of first hidden layer 1000','Relu, dropout 50pct, width of first hidden layer 1000','Sigmoid, dropout 30pct, width of first hidden layer 1000','Sigmoid, dropout 50pct, width of first hidden layer 1000']

for i in range(len(data_list)):
    plt.plot(data_list[i][0],data_list[i][1], 'b', label='train')
    plt.plot(data_list[i][0],data_list[i][2], 'r', label='validation')
    plt.legend()
    plt.title(title_list[i])
    plt.xlabel('Number of hidden layers')
    plt.ylabel('Root mean squared error')
    plt.ylim(0.1,0.6)

    plt.savefig("plots/" + title_list[i] + ".png")
    plt.show()
