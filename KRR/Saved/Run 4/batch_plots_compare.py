import numpy as np
import pickle
import matplotlib.pyplot as plt
import csv
import pandas

folder = "GP/"
ktype = "gauss"
lambd = [0.001,0.01,0.1,1.0,10]
prdf="default"
#Compare shown in red
cfolder = "SimpleLarge/"
cktype = "gauss"
cprdf="default"
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
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+str(l),color="blue")
#Datasset to compare
data=pandas.read_csv(cfolder+cktype+'/'+cprdf+'.csv',', ')
names=list(data)
for l in lambd:
    results = data.loc[data[names[0]] == l]
    x=np.asarray(results[results.columns[1]])
    sort = x.argsort()
    y=np.asarray(results[results.columns[3]]) 
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+str(l),color="red")
plt.xscale('symlog', linthreshx=20)
plt.ylim(0.1,0.5)
plt.legend(loc='upper left')
plt.show()
plt.ion()
plt.title("Laplacian kernel with GP description")
plt.xlabel("Sigma value")
plt.ylabel("rmse [eV/atom]")
