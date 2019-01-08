#!/bin/bash

##Kør på cpu
#BSUB -q hpc

##Navn på job
#BSUB -J kernel3_minitest
##Output fil
#BSUB -o output/kernel3_minitest-%J.out
##Antal kerner
#BSUB -n 1
##Om kernerne må være på forskellige computere
#BSUB -R "span[hosts=1]"
##Ram pr kerne
#BSUB -R "rusage[mem=10GB]"
##Hvor lang tid må den køre hh:mm
#BSUB -W 15:00
##Email når jobbet starter
#BSUB -B
##og stopper
#BSUB -N

module purge
module load python3

python3 KRR/kernel3_minitest.py
