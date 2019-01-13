import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
###LAPLACIAN
##GP
list1=[]
#1.373480422956979e-09, 36648.599278185706
list1.append(["m=10, dr=0.25, s=0.125", 0.2731302766433463])
#3.642051725510088e-12, 30854.58631255132
list1.append(["m=8, dr=0.25, s=0.125",0.27258538013471023])
#1.1199082423998318e-07, 94100.43048329327
list1.append(["m=6, dr=0.25, s=0.25", 0.2765307046619115])
#1.6373914108165823e-07, 5734.433354136593
list1.append(["m=6, dr=0.25, s=0.05", 0.27123541118422895])
##SIMPLE
list2=[]
#0.00013249298095703186, 162.73362731933594
list2.append(["m=10, dr=0.25, s=0.125",0.28721403162474257])
#4.2178161621093924e-05, 194.74493408203125
list2.append(["m=8, dr=0.25, s=0.125", 0.2893102326187375])
#1.7663430785350436e-05, 1622.0285161866777
list2.append(["m=6, dr=0.25, s=0.25", 0.292827988617161])
#1.2098876953124703e-05, 158.2872314453125
list2.append(["m=6, dr=0.25, s=0.05", 0.2924868900444324])
names1=[]
values1=[]
names2=[]
values2=[]
for i in range(len(list1)):
    names1.append(list1[i][0])
    values1.append(list1[i][1])
    names2.append(list2[i][0])
    values2.append(list2[i][1])
val1=np.array(values1)
nam1=np.array(names1)
val2=np.array(values2)
nam2=np.array(names2)
#Setup dataframe
df_rearanged = pd.DataFrame({
    'GP description' : values1,
    'Simple description' : values2
    },index = nam1
)
ax=df_rearanged.plot(kind='bar', color=["C0","orangered"], figsize=(16,8))

plt.legend(bbox_to_anchor=(1,0), loc="lower right", ncol=3, fontsize=16)
plt.xticks(fontsize=17)
plt.yticks(fontsize=15)
plt.ylabel("RMSE [eV/atom]",fontsize=17)
plt.xticks(rotation='30', ha='right')
plt.title("Comparison of descriptions in the laplacian kernel space", fontsize=20)
plt.tight_layout()
plt.savefig('desc_laplace.png',dpi=300)
plt.show()
