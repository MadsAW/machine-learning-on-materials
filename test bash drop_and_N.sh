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
#BSUB -W 10:00
##Email når jobbet starter
#BSUB -B
##og stopper
#BSUB -N


module purge
#module load tensorflow/1.5-cpu-python-3.6.2
module load tensorflow/1.5-gpu-python-3.6.2

N_list=(100,250,500,750,1000)
drop_list=(10,20,30,40,50,60,70,80,90)

for drop in "${drop_list[@]}"
do
	for N in "${N_list[@]}"
	do
		echo $drop
		echo $N
	done
done


