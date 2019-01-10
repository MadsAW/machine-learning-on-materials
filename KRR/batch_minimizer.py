c_list = [[5],[10]]
for prdf in ["default", "faulty", "newest","deep"]:#"default", "faulty", "newest","deep"
    for description in ["GP","SimpleLarge"]:#"GP","SimpleLarge"
        for ktype in ["gaussian","laplacian"]:#,"linear","gaussian","laplacian"
            for lambd in [0.001,0.01]:#0.01, 0.001, 0.1, 10, 1
                for c1 in c_list:
                    #Shell script function
                    jobname='batch_job_this_is_on_purpose_to_utilize_more_kernel'
                    output='output/batch/batchjobs-%J.out'
                    mem='10GB'
                    runtime='45:00'
                    run='KRR/minimizer.py '+ktype+' '+str(lambd)+' '+description+' '+prdf+' '+str(c1)
                    Mailbegin=False
                    Mailend=False
                    mailb,maile="",""
                    if Mailbegin: mailb='\n#BSUB -B'
                    if Mailend: maile='\n#BSUB -N'
                    new_entry='#!/bin/bash\n##Kør på cpu\n#BSUB -q hpc\n##Navn på job\n#BSUB -J '+jobname+'\n##Output fil\n#BSUB -o '+output+'\n##Antal kerner\n#BSUB -n 1\n##Om kernerne må være på forskellige computere\n#BSUB -R "span[hosts=1]"\n##Ram pr kerne\n#BSUB -R "rusage[mem='+mem+']"\n##Hvor lang tid må den køre hh:mm\n#BSUB -W '+runtime+'\n##Email når jobbet starter'+mailb+'\n##og stopper'+maile+'\nmodule purge\nmodule load python3\npython3 '+run
                    #Shell script name
                    file="first_batch_"+prdf+"_"+description+"_"+ktype+"_"+str(lambd)+"_"+str(c1)
                    with open("Shellscripts/batch/2/"+file+".sh", "w+",encoding='utf-8') as g:
                        g.write(new_entry)
