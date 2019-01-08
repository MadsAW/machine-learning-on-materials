#!/bin/bash

##Kør på cpu
#BSUB -q hpc

##Navn på job
#BSUB -J kernel_script
##Output fil
#BSUB -o output/kernel_script-%J.out
##Antal kerner
#BSUB -n 1
##Om kernerne må være på forskellige computere
#BSUB -R "span[hosts=1]"
##Ram pr kerne
#BSUB -R "rusage[mem=10GB]"
##Hvor lang tid må den køre hh:mm
#BSUB -W 24:00
##Email når jobbet starter
#BSUB -B
##og stopper
#BSUB -N

module purge
module load python3

python3 KRR/kernel_script.py
