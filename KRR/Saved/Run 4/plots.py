import numpy as np
import pickle
import matplotlib.pyplot as plt
folder = "GP/"
ktype = "lin/"
matrix = "4_lin_val_0.01"
with open(folder+ktype+matrix, "rb") as pickleFile:
    results = pickle.load(pickleFile)
    # Enable interactive mode
    plt.ion()
    
    # Draw the grid lines
    plt.grid(True)
    plt.plot(results[1],results[2])
    plt.xscale('symlog', linthreshx=20)
