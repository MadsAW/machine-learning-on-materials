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


relu=[]
sigmoid=[]
fol03_01=[]
fol04_01=[]
fol11_10=[]
fol09_01=[]
grpprdxgrpprd=[]
anumxanum=[]
grpprdgrpprd2x2=[]
for di in data:
    if di['acti']=='relu':
        relu.append(di['rmse_val'])
    if di['acti']=='sigmoid':
        sigmoid.append(di['rmse_val'])    
    if di['m_folder']=='03-01-2019 11.04':
        fol03_01.append(di['rmse_val'])
    if di['m_folder']=='04-01-2019 21.56':
        fol04_01.append(di['rmse_val'])
    if di['m_folder']=='11-10-2018 11.36':
        fol11_10.append(di['rmse_val'])
    if di['m_folder']=='09-01-2019 12.57':
        fol09_01.append(di['rmse_val'])
    if di['m_func']=='shape_group_period_x_group_period':
        grpprdxgrpprd.append(di['rmse_val'])
    if di['m_func']=='shape_atomic_number':
        anumxanum.append(di['rmse_val'])
    if di['m_func']=='shape_group_period_2x2':
        grpprdgrpprd2x2.append(di['rmse_val'])

relu=np.mean(relu)
sigmoid=np.mean(sigmoid)
fol03_01=np.mean(fol03_01)
fol04_01=np.mean(fol04_01)
fol11_10=np.mean(fol11_10)
fol09_01=np.mean(fol09_01)
grpprdxgrpprd=np.mean(grpprdxgrpprd)
anumxanum=np.mean(anumxanum)
grpprdgrpprd2x2=np.mean(grpprdgrpprd2x2)

mean_list={'acti':[relu,sigmoid], 'm_folder':[fol03_01,fol04_01,fol11_10,fol09_01], 'm_func':[anumxanum,grpprdgrpprd2x2,grpprdxgrpprd]}

for param in ['N','drop','nhidden']:
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
    
    plt.plot(l1,l2)

    
    plt.title(param)
    plt.show()
    

values={'acti':['sigmoid','relu'],'m_folder':['03-01-2019 11.04','04-01-2019 21.56','11-10-2018 11.36','09-01-2019 12.57'],'m_func':['shape_group_period_x_group_period','shape_atomic_number','shape_group_period_2x2']}
for param in ['acti','m_folder','m_func']:
    l1=values[param]
    l2=[]
    
    for val in l1:
        sublist=[di['rmse_val'] for di in data if di[param]==val]
        try:
            best=min(sublist)
        except:
            best=0
        l2.append(best)
    
    

    plt.bar(l1,l2)
    plt.xticks(rotation='30')
    plt.show()
    
