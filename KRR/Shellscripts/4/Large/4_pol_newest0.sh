#!/bin/bash

##Kør på cpu
#BSUB -q hpc

##Navn på job
#BSUB -J KRR_4_newest_pol
##Output fil
#BSUB -o output/4_0.1_newest_pol-%J.out
##Antal kerner
#BSUB -n 1
##Om kernerne må være på forskellige computere
#BSUB -R "span[hosts=1]"
##Ram pr kerne
#BSUB -R "rusage[mem=6GB]"
##Hvor lang tid må den køre hh:mm
#BSUB -W 45:00
##Email når jobbet starter
#BSUB -B
##og stopper
#BSUB -N

module purge
module load python3

python3 KRR/KRR_script_4_newest.py polynomial 0.1 SimpleLarge
