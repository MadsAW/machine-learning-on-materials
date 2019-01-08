import numpy as np
import pickle
import matplotlib.pyplot as plt
folder = "GP/"
ktype = "laplace"
matrix = "/4_"+ktype+"_val_0.01"
with open(folder+ktype+matrix, "rb") as pickleFile:
    results = pickle.load(pickleFile)
    arrray = results[2]
    # Enable interactive mode
    plt.ion()
    
    # Draw the grid lines
    plt.grid(True)
    plt.plot(results[1],results[2])
    plt.xscale('symlog', linthreshx=20)
