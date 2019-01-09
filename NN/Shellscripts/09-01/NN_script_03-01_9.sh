#!/bin/bash
##Kør på gpu
#BSUB -q gpuv100
##Antal gpuer vi vil bruge. Kommenter ud hvis cpu.
#BSUB -gpu "num=1:mode=exclusive_process"

##Kør på cpu
##BSUB -q hpc

##Navn på job
#BSUB -J NN_last
##Output fil
#BSUB -o output/NN_last-%J.out
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


for drop in 0 0.1 0.2 0.25 0.3 0.4 0.7
do
	for N in 450
	do
		for nhidden in 0 1 2 3 4 5 6
		do
			for act in sigmoid
			do
				for folder in 09-01-201912.57
				do
					for func in group_period_x_group_period group_period_2x2 atomic_number
					do
						python3 NN/NN_script.py $drop 450 sigmoid $nhidden 09-01-2019\ 12.57 $func
					done
				done
			done
		done
	done
done
