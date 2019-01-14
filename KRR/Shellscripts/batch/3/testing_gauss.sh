#!/bin/bash
##Kør på cpu
#BSUB -q hpc
##Navn på job
#BSUB -J testing_gauss
##Output fil
#BSUB -o output/test_results_gauss-%J.out
##Antal kerner
#BSUB -n 1
##Om kernerne må være på forskellige computere
#BSUB -R "span[hosts=1]"
##Ram pr kerne
#BSUB -R "rusage[mem=10GB]"
##Hvor lang tid må den køre hh:mm
#BSUB -W 45:00
##Email når jobbet starter
#BSUB -B
##og stopper
#BSUB -N
module purge
module load python3
python3 KRR/KRR_on_test.py gaussian 0.8193310105066505 GP newest -0.0004232564074429044