#!/bin/bash
##Kør på gpu
#BSUB -q gpuv100
##Kør på cpu
##BSUB -q hpc
##Antal gpuer vi vil bruge. Kommenter ud hvis cpu.
#BSUB -gpu "num=1:mode=exclusive_process"
##Navn på job
#BSUB -J test2
##Output fil
#BSUB -o test2-%J.out
##Antal kerner
#BSUB -n 8
##Om kernerne må være på forskellige computere
#BSUB -R "span[hosts=1]"
##Ram pr kerne
#BSUB -R "rusage[mem=3GB]"
##Hvor lang tid må den køre hh:mm
#BSUB -W 10:00
##Email når jobbet starter
#BSUB -B
##og stopper
#BSUB -N


module purge
module load tensorflow/1.5-cpu-python-3.6.2

python3 test2.py

