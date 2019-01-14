import numpy as np
import pickle
import matplotlib.pyplot as plt
import csv
import pandas

folder = "GP/"
ktype = "lin"
lambd = [0.01,0.1,1.0]

prdf="newest"
data=pandas.read_csv(folder+ktype+'/'+prdf+'.csv',', ')
names=list(data)
plt.figure(0,figsize=(20,6))
# Enable interactive mode
plt.ion()
plt.title("Linear kernel with GP description",fontsize=20)
plt.xlabel("first coefficient (c) value",fontsize=17)
plt.ylabel("RMSE [eV/atom]",fontsize=17)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
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
plt.legend(loc='upper left', fontsize=17)
plt.show()
plt.savefig('kernel_lin.png')
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
plt.legend(loc='lower right')
plt.title("Effect of Regularization", fontsize=20)
plt.tight_layout()
plt.savefig("lin_lam.png")
plt.show()


#GAUSS
lambd = [0.001,0.01,0.1]
ktype="gauss"
data=pandas.read_csv(folder+ktype+'/'+prdf+'.csv',', ')
names=list(data)
plt.figure(1)
# Enable interactive mode
plt.ion()
plt.title("Gaussian kernel with GP description", fontsize=20)
plt.xlabel("Sigma value", fontsize=17)
plt.ylabel("RMSE [eV/atom]", fontsize=17)
# Draw the grid lines
plt.grid(True)
for l in lambd:
    results = data.loc[data[names[0]] == l]
    x=np.asarray(results[results.columns[1]])
    sort = x.argsort()
    y=np.asarray(results[results.columns[3]]) 
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+str(l))
plt.ylim(0.2,0.7)
plt.legend(loc='lower right', fontsize=17)
plt.savefig("kernel_gauss.png")
plt.show()
plt.figure(4)
# Enable interactive mode
plt.ion()
plt.title("Gaussian kernel with GP description", fontsize=20)
plt.xlabel("Lambda value", fontsize=17)
plt.ylabel("RMSE [eV/atom]", fontsize=17)
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
plt.legend(loc='lower right', fontsize=17)
plt.title("Gaussian kernel with GP description", fontsize=20)

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
plt.ylabel("RMSE [eV/atom]")
# Draw the grid lines
plt.grid(True)
for l in lambd:
    results = data.loc[data[names[0]] == l]
    x=np.asarray(results[results.columns[1]])
    sort = x.argsort()
    y=np.asarray(results[results.columns[3]]) 
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=2, markersize=8, label="using lambda = "+str(l))
plt.ylim(0.2,0.7)
plt.legend(loc='upper left', fontsize=17)
plt.savefig("kernel_lap.png")
plt.show()
#TRAINING AND VALIDATION SET PLOTS
plt.figure(5)
# Enable interactive mode
plt.ion()
plt.title("Laplacian kernel with GP description", fontsize=20)
plt.xlabel("Lambda value", fontsize=17)
plt.ylabel("RMSE [eV/atom]", fontsize=17)
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
plt.legend(loc='lower right', fontsize=17)
plt.title("Laplacian kernel with GP description", fontsize=20)
plt.savefig("laplace_lam.png")
plt.show()


