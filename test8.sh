#!/bin/bash
##Kør på gpu
#BSUB -q gputitanxpascal
##Antal gpuer vi vil bruge. Kommenter ud hvis cpu.
#BSUB -gpu "num=1:mode=exclusive_process"

##Kør på cpu
##BSUB -q hpc

##Navn på job
#BSUB -J test8
##Output fil
#BSUB -o test8-%J.out
##Antal kerner
#BSUB -n 8
##Om kernerne må være på forskellige computere
#BSUB -R "span[hosts=1]"
##Ram pr kerne
#BSUB -R "rusage[mem=3GB]"
##Hvor lang tid må den køre hh:mm
#BSUB -W 15:00
##Email når jobbet starter
#BSUB -B
##og stopper
#BSUB -N


module purge
#module load tensorflow/1.5-cpu-python-3.6.2
module load tensorflow/1.5-gpu-python-3.6.2

python3 test8.py

