# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 09:24:07 2019

@author: madsa
"""
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import matplotlib
import pickle
import matplotlib.tri as mtri

path = "Saved/kernel pickles/"
matrix="2_lin_val"
with open(path+matrix, "rb") as pickleFile:
    results = pickle.load(pickleFile)
    A=results[len(results)-1]

    # Make data.
    x = results[len(results)-3]
    y = results[len(results)-2]

    hf = plt.figure()
    ha = hf.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(x, y)  # `plot_surface` expects `x` and `y` data to be 2D
    ha.plot_surface(X, Y, A)

    plt.show()
    # Plot the surface.
    #surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
    """                 linewidth=0, antialiased=False)
triang = mtri.Triangulation(x, y)
fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection='3d')

ax.plot_trisurf(triang, z, cmap='jet')
ax.scatter(x,y,z, marker='.', s=10, c="black", alpha=0.5)
ax.view_init(elev=60, azim=-45)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()"""
"""#%% Load training data
matrix=".npy"

    ax.imshow(masked_array, interpolation='nearest', cmap=cmap)
    Axes3D.plot_surface(X, Y, Z, *args, **kwargs)
    
 
    
    A[A==-1]=np.nan
    where_are_NaNs = np.isnan(A)
    A[where_are_NaNs] = 100
    index=np.unravel_index(A.argmin(), A.shape)
    print(matrix+" best result is:", A[index])
     print("At index: " + str(index))
        dimensions=[]
        for i in range(1,len(results)-1):
            dimensions.append(results[i])
        Variables=[]
        for i in range(len(dimensions)):
            Variables.append(dimensions[i][index[i]])
        print("Variables:", Variables)
        print("Lambda:", results[0][index[-1]])
"""