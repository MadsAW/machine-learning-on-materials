#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 09:31:28 2018

@author: Simon
"""

#from kernel_functions_load import *
import pickle
import numpy as np

folder = 'kernel pickles/'



#%%
#Linear
c_list = [10**n for n in range(-2,5)]
x = [-10**n for n in range(-2,5)]
x.reverse()
c_list = x + c_list

lam_list = [10**n for n in range(-2,5)]

with open(folder+'out_matrix_lin', 'rb') as file:
    lin_matrix = pickle.load(file)
    
min_val = np.min(lin_matrix)
min_index = np.argwhere(lin_matrix==min_val)

#Best values based on training rmse:
ind=min_index[0]
print(f'linear, min training rmse={min_val}, c={c_list[ind[0]]}, lambda={lam_list[ind[1]]}')

#%%
#Polynomial
c1_list = [10**n for n in range(-2,2)]

c2_list = [10**n for n in range(-2,2)]
x = [10**n for n in range(-2,2)]
x.reverse()
c2_list = x + c2_list

d_list = [10**n for n in range(-2,2)]

lam_list = [10**n for n in range(-2,2)]

with open(folder+'out_matrix_pol', 'rb') as file:
    pol_matrix = pickle.load(file)

min_val = np.min(pol_matrix)
min_index = np.argwhere(pol_matrix==min_val)

#Best values based on training rmse:
ind=min_index[0]
print(f'polynomial, min training rmse={min_val}, c1={c1_list[ind[0]]}, c2={c2_list[ind[1]]}, d={d_list[ind[2]]} lambda={lam_list[ind[3]]}')





#%%
#Gaussian
sigma_list = [10**n for n in range(-2,2)]

lam_list = [10**n for n in range(-2,2)]

with open(folder+'out_matrix_gauss', 'rb') as file:
    gauss_matrix = pickle.load(file)

min_val = np.min(gauss_matrix)
min_index = np.argwhere(gauss_matrix==min_val)


#Best values based on training rmse:
ind=min_index[0]
print(f'gaussian, min training rmse={min_val}, sigma={sigma_list[ind[0]]}, lambda={lam_list[ind[1]]}')


#%%
#Laplacian
sigma_list = [10**n for n in range(-2,2)]

lam_list = [10**n for n in range(-2,2)]

with open(folder+'out_matrix_laplace', 'rb') as file:
    laplace_matrix = pickle.load(file)

min_val = np.min(laplace_matrix)
min_index = np.argwhere(laplace_matrix==min_val)


#Best values based on training rmse:
ind=min_index[0]
print(f'laplacian, min training rmse={min_val}, sigma={sigma_list[ind[0]]}, lambda={lam_list[ind[1]]}')
