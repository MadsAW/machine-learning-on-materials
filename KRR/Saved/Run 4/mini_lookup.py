import numpy as np
import pickle
import matplotlib.pyplot as plt
import os
import fnmatch
folder = "GP/"
ktype = "lin/"
matrices=os.listdir(folder+ktype)

for matrix in matrices:
    if fnmatch.fnmatch(matrix, 'MINI_*'):
        with open(folder+ktype+matrix, "rb") as pickleFile:
            results = pickle.load(pickleFile)
            # Enable interactive mode
            plt.ion()
            print(results)
            # Draw the grid lines
            plt.grid(True)
            #plt.plot(results[1],results[2],label=matrix)
            plt.xscale('symlog', linthreshx=20)
            #plt.legend(loc='upper left')
