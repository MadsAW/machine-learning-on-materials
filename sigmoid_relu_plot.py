#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 01:03:36 2019

@author: simon
"""
import math
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    return 1/(1+math.exp(-z))

def relu(z):
    return max(0,z)

x=np.arange(-10,10,0.01)
y1=np.array(list(map(sigmoid, x)))
y2=np.array(list(map(relu, x)))


ax=plt.axes()
plt.text(0.05,0.9,r'$\sigma (z)=\frac{1}{1+e^{-z}}$',size=20, transform=ax.transAxes)
plt.text(-0.1,-0.13,'(a)',size=16, transform=ax.transAxes)
plt.xticks(np.arange(-10,11,5), fontsize=14)
plt.yticks(fontsize=14)
plt.title('Sigmoid', fontsize=16)
plt.plot(x,y1)
plt.savefig('sigmoid.png',dpi=300)
plt.show()


ax=plt.axes()
plt.text(0.05,0.9,'$R(z)=max(0,z)$',size=20, transform=ax.transAxes)
plt.text(-0.1,-0.13,'(b)',size=16, transform=ax.transAxes)
plt.xticks(np.arange(-10,11,5),fontsize=14)
plt.yticks(fontsize=14)
plt.title('ReLU', fontsize=16)
plt.plot(x,y2)
plt.savefig('relu.png',dpi=300)