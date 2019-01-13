import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
###GASSIAN GOOD GLOBAL MINIMIM INDICATE NO LOCAL MINIMA
##GP
list1=[]

#0.007111849895570986, 3.6680395237441648
list1.append(["m=10, dr=0.25, s=0.125",0.2656761258075269])
#0.009046327104499655, 3.5622800481516506
list1.append(["m=8, dr=0.25, s=0.125",0.26402949852507074])
#0.014489053279873196, 2.132286812209018
list1.append(["m=6, dr=0.25, s=0.25", 0.27305786209504607])
#0.010058079020921623, 7.2388155580011855
list1.append(["m=6, dr=0.25, s=0.05", 0.263071580871078])
##SIMPLE WAIT FOR RESULTS TOMORROW
list2=[]
#0.00036982421874999776, 17.100830078125
list2.append(["m=10, dr=0.25, s=0.125",0.2800127159014104])
#1.775976562500004e-05, 57.232421875
list2.append(["m=8, dr=0.25, s=0.125",0.28047240366221854])
#2.2104256092291447e-05, 52.712484975941464
list2.append(["m=6, dr=0.25, s=0.25", 0.28790515409470496])
#1.1843750000000003e-05, 16.78125
list2.append(["m=6, dr=0.25, s=0.05", 0.2859181052021272])
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
plt.title("Comparison of descriptions in the gaussian kernel space", fontsize=20)
plt.tight_layout()
plt.savefig('desc_gauss.png',dpi=300)
plt.show()
