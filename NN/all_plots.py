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
from matplotlib.ticker import MaxNLocator

os.chdir("Saved")

folders = [f for f in os.listdir() if f!='Old saved' and f!='.DS_Store' and f!='best']
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

histories=[]
for di in data:
    path=di['m_folder']+'_'+di['m_func']+'/'+di['file']
    with open(path, 'rb') as pickle_file:
        history=pickle.load(pickle_file)
    histories.append(history['val_mean_squared_error'])
    di['rmse']=np.sqrt(np.mean(history['mean_squared_error'][-10:]))
    di['rmse_val']=np.sqrt(np.mean(history['val_mean_squared_error'][-10:]))


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
fol09_01ny=[]
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
    if di['m_folder']=='09-01-2019 16.03':
        fol09_01ny.append(di['rmse_val'])
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
fol09_01ny=np.mean(fol09_01ny)
grpprdxgrpprd=np.mean(grpprdxgrpprd)
anumxanum=np.mean(anumxanum)
grpprdgrpprd2x2=np.mean(grpprdgrpprd2x2)

mean_list={'acti':[relu,sigmoid], 'm_folder':[fol03_01,fol04_01,fol11_10,fol09_01,fol09_01ny], 'm_func':[anumxanum,grpprdgrpprd2x2,grpprdxgrpprd]}
sub_letters={'N':'(a)','drop':'(c)','nhidden':'(b)','m_folder':'(a)','m_func':'(b)','acti':''}
titles={'N':'RMSE vs. size of first hidden layer','drop':'RMSE vs. dropout regularization','acti':'Activation function','nhidden':'RMSE vs. number of hidden layers','m_folder':'PRDF parameters','m_func':'Feature matrix shape'}
xlabels={'N':'Layer size','drop':'Dropout value','nhidden':'Number of hidden layers'}
for param in ['N','drop','nhidden']:
    new_list = param_list.copy()
    new_list.pop(param_list.index(param))

    plot_list=[]
    for di in data:
        if [di[p] for p in new_list]==[minimum_di[p] for p in new_list]:
            plot_list.append(di)



    list_param=[di[param] for di in plot_list]
    list_rmse=[di['rmse_val'] for di in plot_list]
    list_train=[di['rmse'] for di in plot_list]

    l1,l2=zip(*sorted(zip(list_param, list_rmse)))
    l1=list(l1)
    l2=list(l2)

    l1,l2_train=zip(*sorted(zip(list_param, list_train)))
    l1=list(l1)
    l2_train=list(l2_train)
    
    
    
    if param=='nhidden':
        l1.pop(0)
        l2.pop(0)
        l2_train.pop(0)
        ax = plt.figure().gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    else:
        ax=plt.axes()
    
    plt.plot(l1,l2)
    plt.plot(l1,l2_train, color='orangered')
    plt.legend(['Validation','Training'])


    plt.title(titles[param],fontsize=16)
    plt.ylabel('RMSE [eV/atom]',fontsize=14)
    plt.xlabel(xlabels[param],fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    plt.text(-0.1,-0.13,sub_letters[param],size=16, transform=ax.transAxes)
    plt.savefig(f'../Plots/{param}.png',dpi=300)
    plt.show()


values={'acti':['sigmoid','relu'],'m_folder':['04-01-2019 21.56','11-10-2018 11.36','09-01-2019 12.57','03-01-2019 11.04','09-01-2019 16.03'],'m_func':['shape_group_period_x_group_period','shape_atomic_number','shape_group_period_2x2']}

tick_names={'sigmoid':'sigmoid','relu':'relu','03-01-2019 11.04':'m=8, dr=0.25, s=0.125','04-01-2019 21.56':'m=6, dr=0.25, s=0.05','11-10-2018 11.36':'m=6, dr=0.25, s=0.25','09-01-2019 12.57':'m=6, dr=0.25, s=0.125','09-01-2019 16.03':'m=10, dr=0.25, s=0.125','shape_group_period_x_group_period':'GP','shape_atomic_number':'Simple','shape_group_period_2x2':'Naive'}
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


    m_list=[]
    for val in l1:
        m=[]
        for di in data:
            if di[param]==val:
                m.append(di['rmse_val'])
        m_list.append(np.mean(m))


    ticks=[tick_names[name] for name in l1]
    plt.bar(ticks,m_list,color='orangered')
    plt.bar(ticks,l2)

    plt.legend(['Mean','Best'], loc='lower right')
    
    if param == 'm_folder':
        plt.xticks(rotation='30', ha='right')
    if param== 'acti':
        print(f"{l1[0]}={l2[0]:.4}, {l1[1]}={l2[1]:.4}")
    plt.title(titles[param],fontsize=16)
    plt.ylabel('RMSE [eV/atom]',fontsize=14)

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.text(-0.1,-0.2,sub_letters[param],size=16, transform=ax.transAxes)
    plt.savefig(f'../Plots/{param}.png',dpi=300)
    plt.show()


#for param in ['nhidden']:
#    new_list = param_list.copy()
#    new_list.pop(param_list.index(param))
#
#    x0=[]
#    for di in data:
#        if di['nhidden']==0:
#            x0.append(di)
#
#    x1=[]
#    for di in data:
#        for x in x0:
#            if [di[p] for p in new_list]==[x[p] for p in new_list] and di['nhidden']==1:
#                x1.append(di)
#
#
#
#    ordered_x1=[]
#    for i in range(len(x0)):
#        for j in range(len(x1)):
#            if [x0[i][p] for p in new_list]==[x1[j][p] for p in new_list]:
#                ordered_x1.append(x1[j])
#
#    diff=[]
#    for i in range(len(x0)):
#        diff.append(x0[i]['rmse_val']-ordered_x1[i]['rmse_val'])


#import random
#plt.plot(histories[random.randint(0,len(histories))])
