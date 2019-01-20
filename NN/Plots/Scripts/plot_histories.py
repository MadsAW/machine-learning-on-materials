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

os.chdir("Saved/histories")

files = [file for file in os.listdir() if file!='plots' and file!='.DS_Store']
for file in files:
    with open(file, "rb") as pickleFile:
        history = pickle.load(pickleFile)

    rmse_train = [elem**(1/2) for elem in history['mean_squared_error']]
    rmse_val = [elem**(1/2) for elem in history['val_mean_squared_error']]

    plt.plot(rmse_train, 'b', label='train')
    plt.plot(rmse_val, 'r', label='validation')
    plt.legend()
    plt.xlabel('epochs')
    plt.ylabel('Root mean squared error')
    plt.ylim(0.1,0.6)
    plt.savefig('plots/'+file+'.png')
    plt.show()
