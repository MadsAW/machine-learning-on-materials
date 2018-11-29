#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 14:40:54 2018

@author: Simon
"""

from kernel_functions_load import *


#Define parameters
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


sigma_list = [2**n for n in range(-5,12)]

train_bool = True
#Linear
param_list = c_list

out_matrix_lin = np.zeros((len(param_list), len(lam_list)))
for p in range(len(param_list)):
    for l in range(len(lam_list)):
        try:
            out=calc(lin, param_list[p], lam_list[l], train_bool)[0]
        except:
            out=10e10

        out_matrix_lin[p,l]=out

        

#Pol
params = (c1_list, c2_list, d_list)

out_matrix_pol = np.zeros((len(params[0]), len(params[1]), len(params[2]), len(lam_list)))
for p0 in range(len(params[0])):
    for p1 in range(len(params[0])):
        for p2 in range(len(params[0])):
            for l in range(len(lam_list)):
                tup = (params[0][p0],params[1][p1],params[2][p2])
                try:
                    out=calc(pol, tup, lam_list[l], train_bool)[0]
                except:
                    out=10e10

                out_matrix_pol[p0,p1,p2,l]=out
        

#gauss
param_list = sigma_list

out_matrix_gauss = np.zeros((len(param_list), len(lam_list)))
for p in range(len(param_list)):
    for l in range(len(lam_list)):
        try:
            out=calc(gauss, param_list[p], lam_list[l], train_bool)[0]
        except:
            out=10e10

        out_matrix_gauss[p,l]=out

        
#laplacian
param_list = sigma_list

out_matrix_laplace = np.zeros((len(param_list), len(lam_list)))
for p in range(len(param_list)):
    for l in range(len(lam_list)):
        try:
            out=calc(laplace, param_list[p], lam_list[l], train_bool)[0]
        except:
            out=10e10

        out_matrix_laplace[p,l]=out   
        
        
folder = "kernel pickles/"
with open(folder + "out_matrix_lin", 'wb') as file:
    pickle.dump(out_matrix_lin, file)

with open(folder + "out_matrix_pol", 'wb') as file:
    pickle.dump(out_matrix_pol, file)

with open(folder + "out_matrix_gauss", 'wb') as file:
    pickle.dump(out_matrix_gauss, file)

with open(folder + "out_matrix_laplace", 'wb') as file:
    pickle.dump(out_matrix_laplace, file)