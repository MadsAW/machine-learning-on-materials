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

os.chdir("Saved")

folders = [f for f in os.listdir() if f!='Old saved' and f!='.DS_Store']
folders.sort()


#
folders = folders[-3:]
#



data=[]
for folder in folders:
    files = [file[7:] for file in os.listdir(folder) if file!='.DS_Store']
    
    m_folder=folder[:16]
    m_func=folder[folder.find('_')+1:]

    for file in files:
        N=int(file[:file.find('_')])
        drop=float(file[file.find('drop')+5:file.find('acti')-1])
        if 'relu' in file:
            acti='relu'
        elif 'sigmoid' in file:
            acti='sigmoid'
        nhidden=int(file[-1])
    
        data.append({'N':N,'drop':drop,'acti':acti,'nhidden':nhidden,'m_folder':m_folder,'m_func':m_func,'file':'hist_N_'+file})


for di in data:
    path=di['m_folder']+'_'+di['m_func']+'/'+di['file']
    with open(path, 'rb') as pickle_file:
        history=pickle.load(pickle_file)
    di['rmse']=np.sqrt(np.mean(history['mean_squared_error'][-5:]))
    di['rmse_val']=np.sqrt(np.mean(history['val_mean_squared_error'][-5:]))

minimum=100
for di in data:
    if di['rmse_val']<minimum:
        minimum=di['rmse_val']
        minimum_di=di


param_list=['N','drop','acti','nhidden','m_folder','m_func']


for param in param_list:
    new_list = param_list.copy()
    new_list.pop(param_list.index(param))
    
    plot_list=[]
    for di in data:
        if [di[p] for p in new_list]==[minimum_di[p] for p in new_list]:
            plot_list.append(di)
    
    list_param=[di[param] for di in plot_list]
    list_rmse=[di['rmse_val'] for di in plot_list]
    
    l1,l2=zip(*sorted(zip(list_param, list_rmse)))
    l1=list(l1)
    l2=list(l2)
    
    if type(l1[0])==str:
        plt.bar(l1,l2)


    else:
        plt.plot(l1,l2)
    
    plt.title(param)
    plt.show()
    
    
    
