#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 13:12:03 2018

@author: Simon
"""

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt



os.chdir("Saved/data_size")




files = [file for file in os.listdir() if file!='.DS_Store']

numbers = [int(name[7:]) for name in files]

numbers.sort()

data={0.1:[],0.2:[],0.3:[],0.4:[],0.5:[],0.6:[],0.7:[],0.8:[],0.9:[],1.0:[]}

for num in numbers:
    with open('history'+str(num),'rb') as pickle_file:
        pct, history = pickle.load(pickle_file)
    
    rmse=np.sqrt(np.mean(history['val_mean_squared_error'][-10:]))
    data[float(pct)].append(rmse)


rmse_list=[]

pct_list=list(data.keys())

for pct in pct_list:
    rmse_list.append(np.mean(data[pct]))


ax=plt.axes()
plt.text(-0.1,-0.13,'(a)',size=16, transform=ax.transAxes)

plt.xlabel('% of training set used', fontsize=14)
plt.ylabel('RMSE [eV/atom]', fontsize=14)
plt.ylim(0.24,0.38)
plt.xlim(5,105)
plt.title('RMSE vs. % of training set used (NN)', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.plot(np.array(pct_list)*100,rmse_list, 'x--', linewidth=2, markersize=8)
plt.savefig('../../Plots/RMSE_pct_training', dpi=300)
plt.show()

