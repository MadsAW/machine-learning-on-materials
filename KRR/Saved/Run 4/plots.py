import numpy as np
import pickle
import matplotlib.pyplot as plt
folder = "GP/"
ktype = "lin"
lambd = ["0.01","0.1","1.0"]
prdf="" #Choices are "newest_" (5 overlap), "faulty_" (no overlap) and "" (1/2)
plt.figure(0)   
for l in lambd:
    matrix = "/4_"+prdf+ktype+"_val_"+l
    with open(folder+ktype+matrix, "rb") as pickleFile:
        results = pickle.load(pickleFile)
        array = results[2]
        # Enable interactive mode
        plt.ion()
        plt.title("Linear kernel with GP description")
        plt.xlabel("first coefficient (c) value")
        plt.ylabel("rmse [eV]")
        # Draw the grid lines
        plt.grid(True)
        plt.plot(results[1],results[2], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+l)
        plt.xscale('symlog', linthreshx=20)
        plt.ylim(0.1,0.5)
        plt.legend(loc='upper left')
        plt.show()
plt.figure(1)   
ktype="gauss"
for l in lambd:
    matrix = "/4_"+ktype+"_val_"+l
    with open(folder+ktype+matrix, "rb") as pickleFile:
        results = pickle.load(pickleFile)
        array = results[2]
        # Enable interactive mode
        plt.ion()
        plt.title("Gaussian kernel with GP description")
        plt.xlabel("first coefficient (c) value")
        plt.ylabel("rmse [eV]")
        # Draw the grid lines
        plt.grid(True)
        plt.plot(results[1],results[2], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+l)
        plt.ylim(0.2,0.7)
        plt.legend(loc='upper left')
        plt.show()
        plt.savefig("gauss.png")
ktype="laplace"
plt.figure(2)   
for l in lambd:
    matrix = "/4_"+ktype+"_val_"+l
    with open(folder+ktype+matrix, "rb") as pickleFile:
        results = pickle.load(pickleFile)
        array = results[2]
        # Enable interactive mode
        plt.ion()
        plt.title("Laplacian kernel with GP description")
        plt.xlabel("first coefficient (c) value")
        plt.ylabel("rmse [eV]")
        # Draw the grid lines
        plt.grid(True)
        plt.plot(results[1],results[2], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+l)
        plt.ylim(0.2,0.7)
        plt.legend(loc='upper left')
        plt.show()
        plt.savefig("lap.png")