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


for drop in 0.2 0.25 0.3 0.4
do
	for N in 250 350 400 450 550
	do
		for nhidden in 3
		do
			for act in sigmoid
			do
				for folder in 03-01-2019\ 11.04 09-01-2019\ 12.57 11-10-2018\ 11.36
				do
					for func in group_period_x_group_period group_period_2x2 atomic_number
					do
						python3 NN/NN_script.py $drop $N sigmoid 3 $folder $func
					done
				done
			done
		done
	done
done
