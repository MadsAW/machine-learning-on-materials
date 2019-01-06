import os
import pickle
import numpy as np
from collections import Iterable

path = "Saved/kernel pickles/"

matrices=os.listdir(path)

def flatten(lis):
     for item in lis:
         if isinstance(item, str):
             yield 100
         if isinstance(item, Iterable):
             for x in flatten(item):
                 yield str(x)
         else:        
             yield str(item)
#%% Load training data
#FUCK LAMDA STÅR SOM FØRSTE LISTE MEN ER SIDSTE VÆRDI!!  SOMETHING FISHY
for matrix in matrices:
    with open(path+matrix, "rb") as pickleFile:
        results = pickle.load(pickleFile)
        A=results[len(results)-1]
        A[A==-1]=np.nan
        where_are_NaNs = np.isnan(A)
        A[where_are_NaNs] = 100
        index=np.unravel_index(A.argmin(), A.shape)
        print(matrix+" best result is:", A[index])
        print("At index: " + str(index))
        dimensions=[]
        for i in range(1,len(results)-1):
            dimensions.append(results[i])
        Variables=[]
        for i in range(len(dimensions)):
            Variables.append(dimensions[i][index[i]])
        print("Variables:", Variables)
        print("Lambda:", results[0][index[-1]])
        """
        MANUAL SHIT HERE FOR BACKUP
        values=list(flatten(results[len(results)-1]))
        values = [float((w.replace('nan', "100")).replace("-1","100")) for w in values]
        print(matrix+" best result is: " +str(min(values)))
        index=values.index(min(values))
        print("At index: " + str(index))
        remaining=values
        var=[]
        for i in range(len(results)-1):
            j=int(len(remaining)/len(results[i]))
            step=int(index/j)
            index=index%j
            var.append(step)
            remaining=remaining[step*j:(step+1)*(j)]
        print("Lambda was:",results[0][var[len(var)-1]])
        par=[]
        for i in range(1,len(results)-1):
            par.append(results[i][var[i]])
        print("Other parameters:",par)"""

