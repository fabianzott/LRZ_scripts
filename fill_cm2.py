#!/usr/bin/env python

##################################################################################################################################################
#                                                                                                                                                #
#                   Attention: Specifically for LRZ Linux Cluster, Leibnitz Rechenzentrum, Munich, Germany!                                      #
#                               This script fills the SLURM queue to its maximum number of 50 jobs.                                              #
#                                         run in commandline as:                                                                                 #
#                                             while true; do python3 ~/util/kick/fill_cm2.py; sleep 3600; done                                   #
#                                         This fills queue after every 60 min until all jobs are submitted!                                      #  
#                                                                                                                                                #
#                                               Adjust for other clusters!                                                                       #
#                                               For SLURM Workload Manager                                                                       #
#                                               Compares .com and .log files to determine job status! Run in cwd!                                #
#                                                                                                                                                #
#                                                       Version: 1.00                                                                            #
#                                                                                                                                                #
#                                               Author:         Fabian L. Zott                                                                   #
#                                               Last modified:  16.09.2021                                                                       #
#                                                                                                                                                #
##################################################################################################################################################



import os                       #To find all the filenames use os.listdir()
import glob
import fileinput
import subprocess

cwd = str(os.getcwd())                #get current working directory "cwd"

################################################################################
print("\n" * 4)
print("-----------------------------------------------")
print("------------Hello, beautiful!!-----------------")
print("-----------------------------------------------")
print("\n" * 4)
################Get Information regarding status of queue##################################

calc_on_queue = 'squeue --clusters="clustername" --users="username" -o "%.18i %.9P %.30j %.8u %.2t %.10M %.6D %R" | grep username | wc -l'

calc_count = int(subprocess.getoutput(calc_on_queue))

to_sub_count = 50 - calc_count

print("Number of calculations in queuing system:", calc_count)
print("Number of calculations that can be submitted:", to_sub_count)
print("\n" * 2)

names_on_queue = 'squeue --clusters="clustername" --users="username" -o  "%50j" --noheader'
on_queue = str(subprocess.getoutput(names_on_queue))
list_of_jobs =[]
for line in on_queue.splitlines():
    line = str(line.split()[0])
    list_of_jobs.append(line)
list_of_jobs.pop(0)


##########################Checking .cmd files in folder if already submitted###################

count = 0
directory = os.fsencode(cwd)

if to_sub_count == 0:
    print("Queue is full!!!!")
else:
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".com"):
            basename  = str(os.path.splitext(filename)[0])
            cmd_file = basename + ".cmd"
            log_file = basename + ".log"
            if os.path.exists(cmd_file):
                if not os.path.exists(log_file):
                    if basename not in list_of_jobs:
                        submitt = 'sbatch ' + cmd_file
                        #print(count)
                        os.system(submitt)
                        count = count + 1
                        #print(count)
                        print("Job:", cmd_file, "submitted to queue!")
                        if count >= to_sub_count:
                            print("Number of submitted calculation:", count)
                            break
