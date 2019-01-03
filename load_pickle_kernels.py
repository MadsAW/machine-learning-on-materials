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
with open(folder+'out_matrix_lin', 'rb') as file:
    lam_list, c_list, lin_matrix = pickle.load(file)
    
min_val = np.min(lin_matrix)
min_index = np.argwhere(lin_matrix==min_val)

#Best values based on training rmse:
ind=min_index[0]
print(f'linear, min training rmse={min_val}, c={c_list[ind[0]]}, lambda={lam_list[ind[1]]}')

#%%
#Polynomial
with open(folder+'out_matrix_pol', 'rb') as file:
    lam_list, c1_list, c2_list, d_list, pol_matrix = pickle.load(file)

min_val = np.min(pol_matrix)
min_index = np.argwhere(pol_matrix==min_val)

#Best values based on training rmse:
ind=min_index[0]
print(f'polynomial, min training rmse={min_val}, c1={c1_list[ind[0]]}, c2={c2_list[ind[1]]}, d={d_list[ind[2]]} lambda={lam_list[ind[3]]}')





#%%
#Gaussian
with open(folder+'out_matrix_gauss', 'rb') as file:
    lam_list, sigma_list, gauss_matrix = pickle.load(file)

min_val = np.min(gauss_matrix)
min_index = np.argwhere(gauss_matrix==min_val)


#Best values based on training rmse:
ind=min_index[0]
print(f'gaussian, min training rmse={min_val}, sigma={sigma_list[ind[0]]}, lambda={lam_list[ind[1]]}')


#%%
#Laplacian
with open(folder+'out_matrix_laplace', 'rb') as file:
    lam_list, sigma_list, laplace_matrix = pickle.load(file)

min_val = np.min(laplace_matrix)
min_index = np.argwhere(laplace_matrix==min_val)


#Best values based on training rmse:
ind=min_index[0]
print(f'laplacian, min training rmse={min_val}, sigma={sigma_list[ind[0]]}, lambda={lam_list[ind[1]]}')
