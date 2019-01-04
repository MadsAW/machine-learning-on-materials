#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 14:40:54 2018

@author: Simon
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from createLargerFeatureMatrix import simpleLargeMatrix
from KRR_class import KernelRidgeRegression
import pickle
import numpy as np
import numpy




if len(sys.argv)!=2:
    print('Usage: \n"python3 KRR_script.py method"\nwhere method is one of linear polynomial gaussian laplacian')
    sys.exit(1)

method=sys.argv[1]



path = "Saved matrices/04-01-2019 21.56/sorted_Cutoff25_noSingleElementKrystals/"
#%% Load training data
featureMatrixFile = "train_featureMatrix.npy"
atomicSymbolsListFile = "train_pickledAtomicSymbolsList.txt"
energiesFile = "train_pickledEnergies.txt"

largeFeatureMatrix, mappedAtomicNumber = simpleLargeMatrix(path,featureMatrixFile, atomicSymbolsListFile)


with open(path+energiesFile, "rb") as pickleFile:
    energies = pickle.load(pickleFile)

largeFeatureMatrix.shape = (largeFeatureMatrix.shape[0], -1)

X = largeFeatureMatrix
Y = np.array(energies)

#%% Load validation data
"""
featureMatrixFileValidate = "validate_featureMatrix.npy"
atomicSymbolsListFileValidate = "validate_pickledAtomicSymbolsList.txt"
energiesFileValidate = "validate_pickledEnergies.txt"

largeFeatureMatrixValidate, mappedAtomicNumberValidate = simpleLargeMatrix(path,featureMatrixFileValidate, atomicSymbolsListFileValidate)


with open(path+energiesFileValidate, "rb") as pickleFile:
    energiesValidate = pickle.load(pickleFile)

largeFeatureMatrixValidate.shape = (largeFeatureMatrixValidate.shape[0], -1)

X_v = largeFeatureMatrixValidate
Y_v = np.array(energiesValidate)
"""



#Kernel matrices output folder
folder = "KRR/Saved/kernel pickles/"

#%%
out=1



lam_list = [10**n for n in range(-3,5)]

c_list = [10**n for n in range(-3,7)]
x = [-10**n for n in range(-1,7)]
x.reverse()
c_list = x + c_list

if method=='linear':
    out_matrix_lin = np.zeros((len(c_list), len(lam_list)))
    for c in range(len(c_list)):
        for l in range(len(lam_list)):
            print(f'c={c_list[c]}, lambda={lam_list[l]}', flush=True)

            KRR=KernelRidgeRegression(type="linear")
            KRR.set_var(c1=c_list[c], lamd=lam_list[l])
            KRR.fit(X,Y, "error")
            out=KRR.rmse
            print(out, flush=True)

            out_matrix_lin[c,l]=out


    with open(folder + "out_matrix_lin_fixed_faulty_matrix", 'wb') as file:
        pickle.dump([lam_list, c_list, out_matrix_lin], file)








lam_list = [10**n for n in range(-3,3)]

c1_list = [10**n for n in range(-3,3)]

c2_list = [10**n for n in range(-2,3)]
x = [-10**n for n in range(-2,3)]
x.reverse()
c2_list = x + c2_list

d_list = [10**n for n in range(-3,3)]

if method=='polynomial':
    out_matrix_pol = np.zeros((len(c1_list), len(c2_list), len(d_list), len(lam_list)))
    for c1 in range(len(c1_list)):
        for c2 in range(len(c2_list)):
            for d in range(len(d_list)):
                for l in range(len(lam_list)):
                    print(f'c1={c1_list[c1]}, c2={c2_list[c2]}, d={d_list[d]}, lambda={lam_list[l]}', flush=True)

                    try:
                        KRR=KernelRidgeRegression(type="poly")
                        KRR.set_var(c1=c1_list[c1],c2=c2_list[c2],d=d_list[d], lamd=lam_list[l])
                        KRR.fit(X,Y, "error")
                        out=KRR.rmse
                        print(out, flush=True)
                    except numpy.linalg.linalg.LinAlgError:
                        out=-1
                        print('singular matrix error', flush=True)
                        try:
                            print(f'c1={c1_list[c1]*1.05}, c2={c2_list[c2]*1.05}, d={d_list[d]*1.05}, lambda={lam_list[l]*1.05}', flush=True)
                            KRR=KernelRidgeRegression(type="poly")
                            KRR.set_var(c1=c1_list[c1],c2=c2_list[c2],d=d_list[d], lamd=lam_list[l])
                            KRR.fit(X,Y, "error")
                            out=KRR.rmse
                            print(out, flush=True)
                        except:
                            pass
                    except:
                        pass

                    out_matrix_pol[c1,c2,d,l]=out

    with open(folder + "out_matrix_pol_fixed_faulty_matrix", 'wb') as file:
        pickle.dump([lam_list, c1_list, c2_list, d_list, out_matrix_pol], file)







lam_list = [10**n for n in range(-3,3)]

sigma_list = [10**n for n in range(-3,3)]

if method=='gaussian':
    out_matrix_gauss = np.zeros((len(sigma_list), len(lam_list)))
    for s in range(len(sigma_list)):
        for l in range(len(lam_list)):
            print(f'sigma={sigma_list[s]}, lambda={lam_list[l]}', flush=True)

            KRR=KernelRidgeRegression(type="gauss")
            KRR.set_var(sigma=sigma_list[s], lamd=lam_list[l])
            KRR.fit(X,Y, "error")
            out=KRR.rmse
            print(out, flush=True)


            out_matrix_gauss[s,l]=out


    with open(folder + "out_matrix_gauss_fixed_faulty_matrix", 'wb') as file:
        pickle.dump([lam_list, sigma_list, out_matrix_gauss], file)







lam_list = [10**n for n in range(-3,3)]

sigma_list = [10**n for n in range(-3,3)]

if method=='laplacian':
    out_matrix_laplace = np.zeros((len(sigma_list), len(lam_list)))
    for s in range(len(sigma_list)):
        for l in range(len(lam_list)):
            print(f'sigma={sigma_list[s]}, lambda={lam_list[l]}', flush=True)

            KRR=KernelRidgeRegression(type="laplace")
            KRR.set_var(sigma=sigma_list[s], lamd=lam_list[l])
            KRR.fit(X,Y, "error")
            out=KRR.rmse
            print(out, flush=True)


            out_matrix_laplace[s,l]=out


    with open(folder + "out_matrix_laplace_fixed_faulty_matrix", 'wb') as file:
        pickle.dump([lam_list, sigma_list, out_matrix_laplace], file)
