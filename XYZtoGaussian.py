# python 3.8.8


##################################################################################################################################################
#                                                                                                                                                #
#       This script generates a .com input file (opt + freq) for Gaussian 09 and 16 from .xyz files exported from Maestro, Schrödinger           #
#                                                           after conformer search!                                                              #
#                                                                                                                                                #
#                                               Cluster: Linux Cluster, Leibnitz Rechenzentrum (LRZ), Munich, Germany                            #
#                                               Change method in file!                                                                           #
#                                               Adjust cluster setting!                                                                          #
#                                               Loop over all *.xyz files in current folder!                                                     #
#                                                                                                                                                #
#                                                       Version: 1.12                                                                            #
#                                                                                                                                                #
#                                               Author:         Fabian L. Zott                                                                   #
#                                               Last modified:  16.09.2021                                                                       #
#                                                                                                                                                #
##################################################################################################################################################

import sys
import re
import os
import glob
import fileinput


################Charge and Spinmultiplicity#############

print("\n" * 4)
print("-----------------------------------------------")
print("------------Hello, beautiful!!-----------------")
print("-----------------------------------------------")

print("\n")
print("What charge does your molecule have?")
print("\n")

print("Type as: +1, 0 or -1):")
print("\n")
charge = int(input("Write here: "))
if charge > 0:
    chargestr = "+" + str(charge)
else:
    chargestr = str(charge)
chargestr = str(chargestr)
print("\n")

print("What spinmultiplicity does your molecule have?")
print("\n")
mult = input("Write here: ")
multstr = str(mult)
print("\n" * 2)

print("Charge is:", chargestr, " and spinmultiplicity is:", multstr)
print("\n" * 2)

print("\n")
print("Where do you want to submitt? (cm2_tiny, cm2 or mpp3)")
print("\n" *2)
cluster = input("Write here: ")
clusterstr = str(cluster)


####################Defining Cluster Settings###########
# Leibnitz Rechenzentrum (LRZ), Linux Cluster 09.2021  #


nproc = None
mem = None
cm2 = "cm2"
cm2_tiny = "cm2_tiny"
mpp3 = "mpp3"

if (clusterstr == cm2):
    nproc = "28"
    mem = "48Gb"
    print("%nproc =", nproc,"and %mem =", mem)

elif (clusterstr == cm2_tiny):
    nproc = "28"
    mem = "48Gb"
    print("%nproc =", nproc,"and %mem =", mem)

elif (clusterstr == mpp3):
    nproc = "64"
    mem = "64Gb"
    print("%nproc =", nproc,"and %mem =", mem)

else:
    print("---------Wrong INPUT for Cluster!!!!--------------")
    print("-----------------Try again!-----------------------")
########################################################

print("\n")
print("Good choice!")
print("\n" * 2)

#######################################################

cwd = os.getcwd()                #get current working directory "cwd"
os.chdir(cwd)


for file in glob.glob("*.xyz"):              # parse through *.xyz files generated by Maestro, Schrödinger, LLC, New York, NY, 2021
    filename  = os.path.splitext(file)[0]    # get basenme of .xyz file
    newfile = str(filename) + ".rawxyz"
    fin = open(file,"r")
    lines = fin.readlines()
    fin.close()
    del lines[0:2]
    fout = open(newfile,"w+")
    for line in lines:
        fout.write(line)
    fout.close()

################Creating .com files##################

    com = open(str(filename) + "_SMD_opt_freq.com", "w+")    #create basename.com file and enable for appending text
    com.write("%Nproc=")
    com.write(nproc)
    com.write("\n")
    com.write("%Mem=")
    com.write(mem)
    com.write("\n")
    com.write("%chk=" +  filename + ".chk")
    com.write("\n")
    com.write("#p B3LYP/6-31+G(d,p) opt=tight scrf=(smd,solvent=water) empiricaldispersion=gd3 scf=tight int=finegrid") # method section for optimization
    com.write("\n")
    com.write("")
    com.write("\n")
    com.write(filename +  " opt")
    com.write("\n")
    com.write("")
    com.write("\n")
    com.write(chargestr)
    com.write(" ")
    com.write(multstr)
    com.write("\n")
    with open(filename + ".rawxyz", 'r') as xyzinput:     #open .gjf and print in file
        com.write(xyzinput.read())
    com.write("\n")
    com.write("")
    com.write("\n")
    com.write("")
    com.write("\n")
    com.write("")
    com.write("--link1--")
    com.write("\n")
    com.write("%Nproc=")
    com.write(nproc)
    com.write("\n")
    com.write("%Mem=")
    com.write(mem)
    com.write("\n")
    com.write("%chk=" +  filename + ".chk")
    com.write("\n")
    com.write("#p B3LYP/6-31+G(d,p) freq scrf=(smd,solvent=water) empiricaldispersion=gd3 scf=tight int=finegrid guess=read geom=check") # method section for frequency calculations
    com.write("\n")
    com.write("")
    com.write("\n")
    com.write(filename +  " freq")
    com.write("\n")
    com.write("")
    com.write("\n")
    com.write(chargestr)
    com.write(" ")
    com.write(multstr)
    com.write("\n")
    com.write("")
    com.write("\n")
    com.write("")
    com.write("\n")
    com.write("")

    com.close()     # finish and save file

    if os.path.exists(newfile):
        os.remove(newfile)
    else:
