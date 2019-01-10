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
plt.ion()
plt.title("Laplacian kernel with GP description")
plt.xlabel("Sigma value")
plt.ylabel("rmse [eV/atom]")
# Draw the grid lines
plt.figure(3)
plt.grid(True)
c=100
results = data.loc[data[names[1]] == c]
x=np.asarray(results[results.columns[0]])
sort = x.argsort()
y1=np.asarray(results[results.columns[3]]) 
y2=np.asarray(results[results.columns[2]])
plt.plot(x[sort],y1[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="Cross-validation set")
plt.plot(x[sort],y2[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="Training set")
plt.legend(loc='upper left')
plt.savefig("lap.png")
plt.show()


#GAUSS
lambd = [0.001,0.01,0.1,1.0,10]
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
plt.savefig("gauss.png")
plt.show()
plt.figure(4)
# Enable interactive mode
plt.ion()
plt.title("Gaussian kernel with GP description")
plt.xlabel("Lambda value")
plt.ylabel("rmse [eV/atom]")
# Draw the grid lines
plt.grid(True)
c=5
results = data.loc[data[names[1]] == c]
x=np.asarray(results[results.columns[0]])
sort = x.argsort()
y1=np.asarray(results[results.columns[3]]) 
y2=np.asarray(results[results.columns[2]])
plt.plot(x[sort],y1[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="Cross-validation set")
plt.plot(x[sort],y2[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="Training set")
plt.legend(loc='upper left')
plt.savefig("gauss_lam.png")
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
plt.savefig("lap.png")
plt.show()
#TRAINING AND VALIDATION SET PLOTS
plt.figure(5)
# Enable interactive mode
plt.ion()
plt.title("Laplacian kernel with GP description")
plt.xlabel("Lambda value")
plt.ylabel("rmse [eV/atom]")
# Draw the grid lines
plt.grid(True)
c=5
results = data.loc[data[names[1]] == c]
x=np.asarray(results[results.columns[0]])
sort = x.argsort()
y1=np.asarray(results[results.columns[3]]) 
y2=np.asarray(results[results.columns[2]])
plt.plot(x[sort],y1[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="Cross-validation set")
plt.plot(x[sort],y2[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="Training set")
plt.legend(loc='upper left')
plt.savefig("lap_lam.png")
plt.show()


