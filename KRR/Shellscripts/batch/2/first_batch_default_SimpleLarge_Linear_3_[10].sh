#!/bin/bash
##Kør på cpu
#BSUB -q hpc
##Navn på job
#BSUB -J minimize_batch_job_this_is_on_purpose_to_utilize_more_kernel
##Output fil
#BSUB -o output/minimize/linear_SimpleLarge_default_batchjobs-%J.out
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
module purge
module load python3
python3 KRR/minimizer.py linear 3 SimpleLarge default [10]