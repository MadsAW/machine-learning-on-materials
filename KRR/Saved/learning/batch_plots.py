import numpy as np
import matplotlib.pyplot as plt
import pandas

data=pandas.read_csv('./size2.csv',', ')
names=list(data)
ax=plt.axes()
plt.text(-0.1,-0.13,'(b)',size=16, transform=ax.transAxes)
plt.title("RMSE vs. % of training set used (KRR)",fontsize=16)
plt.xlabel("% of training set used",fontsize=14)
plt.ylabel("RMSE [eV/atom]",fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)


x=[]
y=[]
for l in range(10,110,10):
    results = data.loc[data[names[0]] == l]
    x.append(l)

    y.append(np.min(np.asarray(results[results.columns[2]])))
plt.plot(x,y, marker='x', linestyle='dashed', linewidth=2, markersize=8)
plt.ylim(0.24,0.38)
plt.xlim(5,105)
plt.show()
plt.savefig('learning_curve.png', dpi=300)
#
