#!/bin/bash
##Kør på gpu
#BSUB -q gpuv100
##Antal gpuer vi vil bruge. Kommenter ud hvis cpu.
#BSUB -gpu "num=1:mode=exclusive_process"

##Kør på cpu
##BSUB -q hpc

##Navn på job
#BSUB -J NN_03-01
##Output fil
#BSUB -o output/NN_03-01-%J.out
##Antal kerner
#BSUB -n 5
##Om kernerne må være på forskellige computere
#BSUB -R "span[hosts=1]"
##Ram pr kerne
#BSUB -R "rusage[mem=6GB]"
##Hvor lang tid må den køre hh:mm
#BSUB -W 20:00
##Email når jobbet starter
#BSUB -B
##og stopper
#BSUB -N


module purge
#module load tensorflow/1.5-cpu-python-3.6.2
module load tensorflow/1.5-gpu-python-3.6.2


for drop in 0.35 0.60
do
	for N in 100 400 1000
	do
		for act in relu sigmoid
		do
			for nhidden in 1 2 3
			do
				for feature_matrix_shape in atomic_number group_period_2x2 group_period_x_group_period
				do
					python3 NN/NN_script.py $drop $N $act $nhidden 03-01-2019\ 11.04 $feature_matrix_shape
				done
			done
		done
	done
done
