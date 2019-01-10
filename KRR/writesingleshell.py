
#Shell script function
jobname='testing'
output='output/4_0.1_faulty_gauss-%J.out'
mem='10GB'
runtime='45:00'
run='KRR/KRR_script_4_faulty.py gaussian 0.1 GP'
new_entry='#!/bin/bash\n##Kør på cpu\n#BSUB -q hpc\n##Navn på job\n#BSUB -J '+jobname+'\n##Output fil\n#BSUB -o '+output+'\n##Antal kerner\n#BSUB -n 1\n##Om kernerne må være på forskellige computere\n#BSUB -R "span[hosts=1]"\n##Ram pr kerne\n#BSUB -R "rusage[mem='+mem+']"\n##Hvor lang tid må den køre hh:mm\n#BSUB -W '+runtime+'\n##Email når jobbet starter\n#BSUB -B\n##og stopper\n#BSUB -N\nmodule purge\nmodule load python3\npython3 '+run
#Shell script name
file="test"
with open("Shellscripts/batch/2/"+file+".sh", "w+",encoding='utf-8') as g:
    g.write(new_entry)
