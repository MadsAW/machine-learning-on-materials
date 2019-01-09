c_list = [10**n for n in range(-9,15)]
x = [-10**n for n in range(-9,15)]
x.reverse()
c_list = x + c_list

for prdf in ["default", "faulty", "newest","deep"]:
    for description in ["GP","SimpleLarge"]:
        for ktype in ["linear"]:#,"linear","gaussian","laplacian"
            for lambd in [0.001]:
                for c1 in c_list:
                    #Shell script function
                    jobname='testing'
                    output='output/4_0.1_faulty_gauss-%J.out'
                    mem='10GB'
                    runtime='45:00'
                    run='KRR/batch_KRR.py '+ktype+' '+str(lambd)+' '+description+' '+prdf+' '+str(c1)
                    Mailbegin=False
                    Mailend=True
                    mailb,maile="",""
                    if Mailbegin: mailb='\n#BSUB -B'
                    if Mailend: maile='\n#BSUB -N'
                    new_entry='#!/bin/bash\n##Kør på cpu\n#BSUB -q hpc\n##Navn på job\n#BSUB -J '+jobname+'\n##Output fil\n#BSUB -o '+output+'\n##Antal kerner\n#BSUB -n 1\n##Om kernerne må være på forskellige computere\n#BSUB -R "span[hosts=1]"\n##Ram pr kerne\n#BSUB -R "rusage[mem='+mem+']"\n##Hvor lang tid må den køre hh:mm\n#BSUB -W '+runtime+'\n##Email når jobbet starter'+mailb+'\n##og stopper'+maile+'\nmodule purge\nmodule load python3\npython3 '+run
                    #Shell script name
                    file="first_batch_"+prdf+"_"+description+"_"+ktype+"_"+str(lambd)+"_"+str(c1)
                    with open("Shellscripts/batch/1/"+file+".sh", "w+",encoding='utf-8') as g:
                        g.write(new_entry)
