#!/bin/bash
##Kør på gpu
#BSUB -q gputitanxpascal
##Antal gpuer vi vil bruge. Kommenter ud hvis cpu.
#BSUB -gpu "num=1:mode=exclusive_process"

##Kør på cpu
##BSUB -q hpc

##Navn på job
#BSUB -J systematic_dropout
##Output fil
#BSUB -o systematic_dropout-%J.out
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

python3 drop_0_5.py
python3 drop_0_05.py
python3 drop_0_10.py
python3 drop_0_15.py
python3 drop_0_20.py
python3 drop_0_25.py
python3 drop_0_30.py
python3 drop_0_35.py
python3 drop_0_40.py
python3 drop_0_45.py

