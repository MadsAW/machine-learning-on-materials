#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 14:40:54 2018

@author: Simon
"""
def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

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

featureMatrixFileValidate = "validate_featureMatrix.npy"
atomicSymbolsListFileValidate = "validate_pickledAtomicSymbolsList.txt"
energiesFileValidate = "validate_pickledEnergies.txt"

largeFeatureMatrixValidate, mappedAtomicNumberValidate = simpleLargeMatrix(path,featureMatrixFileValidate, atomicSymbolsListFileValidate)


with open(path+energiesFileValidate, "rb") as pickleFile:
    energiesValidate = pickle.load(pickleFile)

largeFeatureMatrixValidate.shape = (largeFeatureMatrixValidate.shape[0], -1)

Xv = largeFeatureMatrixValidate
Yv = np.array(energiesValidate)




#Kernel matrices output folder
folder = "KRR/Saved/kernel pickles/"

#%%
out=1



lam_list = [10**n for n in range(-1,3)]

c_list = [10**n for n in range(-3,7)]
x = [-10**n for n in range(-1,7)]
x.reverse()
c_list = x + c_list

if method=='linear':
    out1_matrix_lin = np.zeros((len(c_list), len(lam_list)))
    out2_matrix_lin = np.zeros((len(c_list), len(lam_list)))
    for c in range(len(c_list)):
        for l in range(len(lam_list)):
            print(f'c={c_list[c]}, lambda={lam_list[l]}', flush=True)

            KRR=KernelRidgeRegression(type="linear")
            KRR.set_var(c1=c_list[c], lamd=lam_list[l])
            KRR.fit(X,Y, "error")
            out1=KRR.rmse
            KRR.predict(Xv,Yv)
            out2=KRR.rmse
            print("/n Train: " + str(out1) + "Validation: " + str(out2)+"/n", flush=True)

            out1_matrix_lin[c,l]=out1
            out2_matrix_lin[c,l]=out2



    with open(folder + "2_newest_lin_train", 'wb') as file:
        pickle.dump([lam_list, c_list, out1_matrix_lin], file)
    with open(folder + "2_newest_lin_val", 'wb') as file:
        pickle.dump([lam_list, c_list, out2_matrix_lin], file)







lam_list = [10**n for n in range(-1,3)]

c1_list = list(frange(-5,20,5))

c2_list = list(frange(-20,25,10))


d_list = list(frange(-20,25,10))

if method=='polynomial':
    out1_matrix_pol = np.zeros((len(c1_list), len(c2_list), len(d_list), len(lam_list)))
    out2_matrix_pol = np.zeros((len(c1_list), len(c2_list), len(d_list), len(lam_list)))
    for c1 in range(len(c1_list)):
        for c2 in range(len(c2_list)):
            for d in range(len(d_list)):
                for l in range(len(lam_list)):
                    print(f'c1={c1_list[c1]}, c2={c2_list[c2]}, d={d_list[d]}, lambda={lam_list[l]}', flush=True)

                    try:
                        KRR=KernelRidgeRegression(type="poly")
                        KRR.set_var(c1=c1_list[c1],c2=c2_list[c2],d=d_list[d], lamd=lam_list[l])
                        KRR.fit(X,Y, "error")
                        out1=KRR.rmse
                        KRR.predict(Xv,Yv)
                        out2=KRR.rmse
                        print("/n Train: " + str(out1) + "Validation: " + str(out2)+"/n", flush=True)
                    except numpy.linalg.linalg.LinAlgError:
                        out1=-1
                        out2=-1
                        print('singular matrix error', flush=True)
                        try:
                            print(f'c1={c1_list[c1]*1.05}, c2={c2_list[c2]*1.05}, d={d_list[d]*1.05}, lambda={lam_list[l]*1.05}', flush=True)
                            KRR=KernelRidgeRegression(type="poly")
                            KRR.set_var(c1=c1_list[c1],c2=c2_list[c2],d=d_list[d], lamd=lam_list[l])
                            KRR.fit(X,Y, "error")
                            out1=KRR.rmse
                            KRR.predict(Xv,Yv)
                            out2=KRR.rmse
                            print("/n Train: " + str(out1) + "Validation: " + str(out2)+"/n", flush=True)
                        except:
                            pass
                    except:
                        pass

                    out_matrix_pol[c1,c2,d,l]=out

    with open(folder + "2_newest_pol_train", 'wb') as file:
        pickle.dump([lam_list, c1_list, c2_list, d_list, out1_matrix_pol], file)
    with open(folder + "2_newest_pol_val", 'wb') as file:
        pickle.dump([lam_list, c1_list, c2_list, d_list, out2_matrix_pol], file)






lam_list = [10**n for n in range(-1,2)]

sigma_list = [-1,1, 10]

if method=='gaussian':
    out1_matrix_gauss = np.zeros((len(sigma_list), len(lam_list)))
    out2_matrix_gauss = np.zeros((len(sigma_list), len(lam_list)))
    for s in range(len(sigma_list)):
        for l in range(len(lam_list)):
            print(f'sigma={sigma_list[s]}, lambda={lam_list[l]}', flush=True)

            KRR=KernelRidgeRegression(type="gauss")
            KRR.set_var(sigma=sigma_list[s], lamd=lam_list[l])
            out1=KRR.rmse
            KRR.fit(X,Y, "error")
            KRR.predict(Xv,Yv)
            out2=KRR.rmse
            print("/n Train: " + str(out1) + "Validation: " + str(out2)+"/n", flush=True)


            out1_matrix_gauss[s,l]=out1
            out2_matrix_gauss[s,l]=out2


    with open(folder + "2_newest_gauss_train", 'wb') as file:
        pickle.dump([lam_list, sigma_list, out1_matrix_gauss], file)
    with open(folder + "2_newest_gauss_val", 'wb') as file:
        pickle.dump([lam_list, sigma_list, out2_matrix_gauss], file)






lam_list = [10**n for n in range(-1,2)]

sigma_list = [-1,1,10]

if method=='laplacian':
    out1_matrix_laplace = np.zeros((len(sigma_list), len(lam_list)))
    out2_matrix_laplace = np.zeros((len(sigma_list), len(lam_list)))
    for s in range(len(sigma_list)):
        for l in range(len(lam_list)):
            print(f'sigma={sigma_list[s]}, lambda={lam_list[l]}', flush=True)

            KRR=KernelRidgeRegression(type="laplace")
            KRR.set_var(sigma=sigma_list[s], lamd=lam_list[l])
            KRR.fit(X,Y, "error")
            out1=KRR.rmse
            KRR.predict(Xv,Yv)
            out2=KRR.rmse
            print("/n Train: " + str(out1) + "Validation: " + str(out2)+"/n", flush=True)


            out1_matrix_laplace[s,l]=out1
            out2_matrix_laplace[s,l]=out2


    with open(folder + "2_newest_laplace_train", 'wb') as file:
        pickle.dump([lam_list, sigma_list, out1_matrix_laplace], file)
    with open(folder + "2_newest_laplace_val", 'wb') as file:
        pickle.dump([lam_list, sigma_list, out2_matrix_laplace], file)
