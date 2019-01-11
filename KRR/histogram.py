import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
###LINEAR
##GP
list1=[]
#0.5313900008797612, 0.030448488891124725
#0.5345049234114398, 0.02979291446354182
list1.append(["m=10, dr=0.25, s=0.125",0.26922086704684534])
#0.4423911112589919, 56503.99730436048
#0.44238775958797893, -63119.84856580019
#0.4423551094567919, -127848.93607070649 : 0.26761400793811047
#Better 0.45539837423712015, 0.03619787422940135
list1.append(["m=8, dr=0.25, s=0.125",0.2673175138023656])
#0.3077881658694209, 0.00675527563432818
#Trench trend THIS IS GOOD
list1.append(["m=6, dr=0.25, s=0.25", 0.2767980143066039])
#0.8193310105066505, -0.0004232564074429044
list1.append(["m=6, dr=0.25, s=0.05", 0.2614952849039045])
##SIMPLE
list2=[]
#0.11286010742187248, -11636.825561523438
list2.append(["m=10, dr=0.25, s=0.125",0.27993])
#0.06621093749999757, -12950.1953125
list2.append(["m=8, dr=0.25, s=0.125",0.2804547377524538])
#0.0626332662039175, -10728.806991610327 all nums
list2.append(["m=6, dr=0.25, s=0.25", 0.28790199368183184])
#0.12265624999999752, -11595.703125
list2.append(["m=6, dr=0.25, s=0.05", 0.2841870845978778])
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
plt.title("Comparison of descriptions in the linear kernel space", fontsize=20)
plt.tight_layout()
plt.savefig('desc_lin.png',dpi=300)
plt.show()
