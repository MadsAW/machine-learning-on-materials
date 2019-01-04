#!/bin/bash

##Kør på cpu
#BSUB -q hpc

##Navn på job
#BSUB -J kernel_script_class_lap
##Output fil
#BSUB -o kernel_script_class_lap-%J.out
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

python3 kernel_script_class.py laplacian
