#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 09:31:28 2018

@author: Simon
"""

from kernel_functions_load import *

folder = 'kernel pickles/'


#%%
#Parameters
lam_list = [2**n for n in range(-5,12)]


c_list = [2**n for n in range(-5,12)]
x = [-2**n for n in range(-5,12)]
x.reverse()
c_list = x + c_list

c1_list = [2**n for n in range(-5,12)]

c2_list = [2**n for n in range(-5,12)]
x = [-2**n for n in range(-5,12)]
x.reverse()
c2_list = x + c2_list

d_list = [2**n for n in range(0,12)]

sigma_list = [2**n for n in range(-5,8)]


#%%
#Linear
with open(folder+'out_matrix_lin', 'rb') as file:
    lin_matrix = pickle.load(file)
    
min_val = np.min(lin_matrix)
min_index = np.argmin(lin_matrix)

#Best values based on training rmse:
c_list[min_index[0]]
lam_list[min_index[1]]

#%%
#Polynomial
with open(folder+'out_matrix_pol', 'rb') as file:
    pol_matrix = pickle.load(file)

min_val = np.min(pol_matrix)
min_index = np.argmin(pol_matrix)

#Best values based on training rmse:
c1_list[min_index[0]]
c2_list[min_index[1]]
d_list[min_index[2]]
lam_list[min_index[3]]

#%%
#Gaussian
with open(folder+'out_matrix_gauss', 'rb') as file:
    gauss_matrix = pickle.load(file)

min_val = np.min(gauss_matrix)
min_index = np.argmin(gauss_matrix)

#Best values based on training rmse:
sigma_list[min_index[0]]
lam_list[min_index[1]]
#%%
#Laplacian
with open(folder+'out_matrix_laplace', 'rb') as file:
    laplace_matrix = pickle.load(file)

min_val = np.min(laplace_matrix)
min_index = np.argmin(laplace_matrix)

#Best values based on training rmse:
sigma_list[min_index[0]]
lam_list[min_index[1]]