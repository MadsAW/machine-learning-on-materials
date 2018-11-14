#!/bin/bash
##Kør på gpu
#BSUB -q gputitanxpascal
##Antal gpuer vi vil bruge. Kommenter ud hvis cpu.
#BSUB -gpu "num=1:mode=exclusive_process"

##Kør på cpu
##BSUB -q hpc

##Navn på job
#BSUB -J systematic_L2
##Output fil
#BSUB -o systematic_L2-%J.out
##Antal kerner
#BSUB -n 5
##Om kernerne må være på forskellige computere
#BSUB -R "span[hosts=1]"
##Ram pr kerne
#BSUB -R "rusage[mem=6GB]"
##Hvor lang tid må den køre hh:mm
#BSUB -W 3:00
##Email når jobbet starter
#BSUB -B
##og stopper
#BSUB -N


module purge
#module load tensorflow/1.5-cpu-python-3.6.2
module load tensorflow/1.5-gpu-python-3.6.2


python3 L2_0_1.py
python3 L2_0_01.py
python3 L2_0_001.py
python3 L2_0_0001.py
python3 L2_0_5.py
python3 L2_0_05.py
python3 L2_0_005.py
python3 L2_0_0005.py
python3 L2_1.py
python3 L2_5.py

