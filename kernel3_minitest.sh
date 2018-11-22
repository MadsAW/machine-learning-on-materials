#!/bin/bash

##Kør på cpu
#BSUB -q hpc

##Navn på job
#BSUB -J kernel3_minitest
##Output fil
#BSUB -o kernel3_minitest-%J.out
##Antal kerner
#BSUB -n 5
##Om kernerne må være på forskellige computere
#BSUB -R "span[hosts=1]"
##Ram pr kerne
#BSUB -R "rusage[mem=6GB]"
##Hvor lang tid må den køre hh:mm
#BSUB -W 15:00
##Email når jobbet starter
#BSUB -B
##og stopper
#BSUB -N



python3 kernel3_minitest.py
