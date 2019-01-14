
#Shell script function
jobname='testing_laplace'
output='output/test_results_laplace-%J.out'
mem='10GB'
runtime='45:00'
run='KRR/KRR_on_test.py laplacian 0.0000001637 GP newest 5734'
new_entry='#!/bin/bash\n##Kør på cpu\n#BSUB -q hpc\n##Navn på job\n#BSUB -J '+jobname+'\n##Output fil\n#BSUB -o '+output+'\n##Antal kerner\n#BSUB -n 1\n##Om kernerne må være på forskellige computere\n#BSUB -R "span[hosts=1]"\n##Ram pr kerne\n#BSUB -R "rusage[mem='+mem+']"\n##Hvor lang tid må den køre hh:mm\n#BSUB -W '+runtime+'\n##Email når jobbet starter\n#BSUB -B\n##og stopper\n#BSUB -N\nmodule purge\nmodule load python3\npython3 '+run
#Shell script name
file="test"
with open("Shellscripts/batch/3/"+file+".sh", "w+",encoding='utf-8') as g:
    g.write(new_entry)
