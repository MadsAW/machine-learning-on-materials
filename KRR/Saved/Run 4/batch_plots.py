import numpy as np
import pickle
import matplotlib.pyplot as plt
import csv
import pandas

folder = "GP/"
ktype = "lin"
lambd = [0.001,0.01,0.1,1.0,10]
prdf="default"
data=pandas.read_csv(folder+ktype+'/'+prdf+'.csv',', ')
names=list(data)
plt.figure(0)
# Enable interactive mode
plt.ion()
plt.title("Linear kernel with GP description")
plt.xlabel("first coefficient (c) value")
plt.ylabel("rmse [eV/atom]")
# Draw the grid lines
plt.grid(True)
for l in lambd:
    results = data.loc[data[names[0]] == l]
    x=np.asarray(results[results.columns[1]])
    sort = x.argsort()
    y=np.asarray(results[results.columns[3]]) 
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+str(l))
plt.xscale('symlog', linthreshx=20)
plt.ylim(0.1,0.5)
plt.legend(loc='upper left')
plt.show()
#GAUSS
ktype="gauss"
data=pandas.read_csv(folder+ktype+'/'+prdf+'.csv',', ')
names=list(data)
plt.figure(1)
# Enable interactive mode
plt.ion()
plt.title("Gaussian kernel with GP description")
plt.xlabel("Sigma value")
plt.ylabel("rmse [eV/atom]")
# Draw the grid lines
plt.grid(True)
for l in lambd:
    results = data.loc[data[names[0]] == l]
    x=np.asarray(results[results.columns[1]])
    sort = x.argsort()
    y=np.asarray(results[results.columns[3]]) 
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+str(l))
plt.ylim(0.2,0.7)
plt.legend(loc='upper left')
plt.show()
#Laplace
ktype="laplace"
data=pandas.read_csv(folder+ktype+'/'+prdf+'.csv',', ')
names=list(data)
plt.figure(2)
# Enable interactive mode
plt.ion()
plt.title("Laplacian kernel with GP description")
plt.xlabel("Sigma value")
plt.ylabel("rmse [eV/atom]")
# Draw the grid lines
plt.grid(True)
for l in lambd:
    results = data.loc[data[names[0]] == l]
    x=np.asarray(results[results.columns[1]])
    sort = x.argsort()
    y=np.asarray(results[results.columns[3]]) 
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+str(l))
plt.ylim(0.2,0.7)
plt.legend(loc='upper left')
plt.show()