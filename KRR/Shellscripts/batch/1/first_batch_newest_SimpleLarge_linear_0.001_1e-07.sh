#!/bin/bash
##Kør på cpu
#BSUB -q hpc
##Navn på job
#BSUB -J testing
##Output fil
#BSUB -o output/4_0.1_faulty_gauss-%J.out
##Antal kerner
#BSUB -n 1
##Om kernerne må være på forskellige computere
#BSUB -R "span[hosts=1]"
##Ram pr kerne
#BSUB -R "rusage[mem=10GB]"
##Hvor lang tid må den køre hh:mm
#BSUB -W 45:00
##Email når jobbet starter
##og stopper
#BSUB -N
module purge
module load python3
python3 KRR/batch_KRR.py linear 0.001 SimpleLarge newest 1e-07