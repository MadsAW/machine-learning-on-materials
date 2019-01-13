import numpy as np
import pickle
import matplotlib.pyplot as plt
folder = "GP/"
ktype = "lin"
lambd = ["0.01","0.1","1.0"]
prdf="newest_" #Choices are "newest_" (5 overlap), "faulty_" (no overlap) and "" (1/2)
plt.figure(0, figsize=(16,6))   
for l in lambd:
    matrix = "/4_"+prdf+ktype+"_val_"+l
    with open(folder+ktype+matrix, "rb") as pickleFile:
        results = pickle.load(pickleFile)
        array = results[2]
        # Enable interactive mode
        plt.ion()
        plt.title("Linear kernel with GP description",fontsize=20)
        plt.xlabel("Coefficient (c) value",fontsize=17)
        plt.ylabel("RMSE [eV/atom]",fontsize=17)
        # Draw the grid lines
        plt.grid(True)
        plt.plot(results[1],results[2], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+l)
        plt.xscale('symlog', linthreshx=20)
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=15)
        plt.ylim(0.2,0.4)
        plt.legend(loc='upper left',fontsize=16)
        plt.show()
        plt.savefig("kernel_lin.png")
plt.figure(1)   
ktype="gauss"
for l in lambd:
    matrix = "/4_"+ktype+"_val_"+l
    with open(folder+ktype+matrix, "rb") as pickleFile:
        results = pickle.load(pickleFile)
        array = results[2]
        # Enable interactive mode
        plt.ion()
        plt.title("Gaussian kernel with GP description",fontsize=20)
        plt.xlabel("Coefficient ($\sigma$) value",fontsize=17)
        plt.ylabel("RMSE [eV/atom]",fontsize=17)
        # Draw the grid lines
        plt.grid(True)
        plt.plot(results[1],results[2], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+l)
        plt.ylim(0.2,0.7)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.legend(loc='upper right', fontsize=16)
        plt.show()
        plt.tight_layout()
        plt.savefig("kernel_gauss.png")
ktype="laplace"
plt.figure(2)   
for l in lambd:
    matrix = "/4_"+ktype+"_val_"+l
    with open(folder+ktype+matrix, "rb") as pickleFile:
        results = pickle.load(pickleFile)
        array = results[2]
        # Enable interactive mode
        plt.ion()
        plt.title("Laplacian kernel with GP description",fontsize=20)
        plt.xlabel("Coefficient ($\sigma$) value",fontsize=17)
        plt.ylabel("RMSE [eV/atom]",fontsize=17)
        # Draw the grid lines
        plt.grid(True)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.plot(results[1],results[2], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+l)
        plt.ylim(0.2,0.7)
        plt.legend(loc='upper right', fontsize=16)
        plt.tight_layout()
        plt.show()
        plt.savefig("kernel_laplace.png")