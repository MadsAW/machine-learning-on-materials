#!/bin/bash

##Kør på cpu
#BSUB -q hpc

##Navn på job
#BSUB -J KRR_script_lap
##Output fil
#BSUB -o output/KRR_script_lap-%J.out
##Antal kerner
#BSUB -n 5
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

python3 KRR/KRR_script.py laplacian
