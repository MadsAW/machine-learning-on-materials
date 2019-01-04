#!/bin/bash
##Kør på gpu
#BSUB -q gpuv100
##Antal gpuer vi vil bruge. Kommenter ud hvis cpu.
#BSUB -gpu "num=1:mode=exclusive_process"

##Kør på cpu
##BSUB -q hpc

##Navn på job
#BSUB -J drop_N_act_nhidden
##Output fil
#BSUB -o output/drop_N_act_nhidden-%J.out
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


for drop in 0.30 0.50
do
	for N in 25 250 1000
	do
		for act in relu sigmoid
		do
			for nhidden in 1 2 3 4 5
			do
				python3 NN/drop_N_act_nhidden_no_redundancy.py $drop $N $act $nhidden
			done
		done
	done
done
