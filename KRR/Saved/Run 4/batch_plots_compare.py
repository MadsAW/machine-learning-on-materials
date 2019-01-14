import numpy as np
import matplotlib.pyplot as plt
import pandas

folder = "GP/"
ktype = "lin"
lambd = [0.01,0.1,1.0]
prdf="newest"
#Compare shown in red
cfolder = "SimpleLarge/"
cktype = "lin"
cprdf="newest"
data=pandas.read_csv(folder+ktype+'/'+prdf+'.csv',', ')
names=list(data)
plt.figure(0)
# Enable interactive mode
plt.ion()
plt.title("Linear kernel with GP description", fontsize=20)
plt.xlabel("first coefficient (c) value",fontsize=16)
plt.ylabel("rmse [eV/atom]",fontsize=16)
# Draw the grid lines
plt.grid(True)
for l in [1]:
    results = data.loc[data[names[0]] == l]
    x=np.asarray(results[results.columns[1]])
    sort = x.argsort()
    y=np.asarray(results[results.columns[3]]) 
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=3, markersize=8, label="GP"+str(l),color="blue")

#Datasset to compare
data=pandas.read_csv(cfolder+cktype+'/'+cprdf+'.csv',', ')
names=list(data)
for l in [0.1]:
    results = data.loc[data[names[0]] == l]
    x=np.asarray(results[results.columns[1]])
    sort = x.argsort()
    y=np.asarray(results[results.columns[3]]) 
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=3, markersize=8, label="Simple"+str(l),color="red")
plt.xscale('symlog', linthreshx=20)
plt.ylim(0.25,0.35)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.show()

folder = "GP/"
ktype = "lin"
lambd = [0.001,0.01,0.1,1.0,10]
prdf="faulty"
#Compare shown in red
cfolder = "GP/"
cktype = "lin"
cprdf="faulty"
plt.figure(1)
# Enable interactive mode
plt.ion()
plt.title("Linear kernel with GP description", fontsize=20)
plt.xlabel("first coefficient (c) value",fontsize=16)
plt.ylabel("rmse [eV/atom]",fontsize=16)
# Draw the grid lines
plt.grid(True)
for l in lambd:
    results = data.loc[data[names[0]] == l]
    x=np.asarray(results[results.columns[1]])
    sort = x.argsort()
    y=np.asarray(results[results.columns[3]]) 
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=3, markersize=8, label="GP"+str(l),color="blue")

#Datasset to compare
data=pandas.read_csv(cfolder+cktype+'/'+cprdf+'.csv',', ')
names=list(data)
for l in lambd:
    results = data.loc[data[names[0]] == l]
    x=np.asarray(results[results.columns[1]])
    sort = x.argsort()
    y=np.asarray(results[results.columns[3]]) 
    plt.plot(x[sort],y[sort], marker='x', linestyle='dashed', linewidth=3, markersize=8, label="Simple"+str(l),color="red")
plt.xscale('symlog', linthreshx=20)
plt.ylim(0.25,0.35)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.show()