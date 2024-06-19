#!/usr/bin/env python3
'''
Author :        Edouard BECHETOILE, Henso ABREU
Description:    Script to dump hexadecimal ascii data produced by PICMIC0/SAMPIC to an ASCII file 
                "version 1"
'''
import pandas as pd
import numpy as np
import sys
import os
import argparse
import re
import struct
from datetime import date,time
import picmic_modules as prepro
import csv
from termcolor import colored

headers = ["nbPixels","timeStamp1","timeStamp2","listPixels"]
CDW = os.getcwd()   # Actual directory
ascii_files = './data_ascii'

##########################################
def dumpData(list1, list2, list3, list4) :
    myList = []
    myList.append(list1)
    myList.append(list2)
    myList.append(list3)
    myList.append(list4)
    return myList

##########################################
def hex_block_to_decimal(hex_block):
    #hex_digits = hex_block.replace('.', '')  # Remove the point if present
    # Extract the first 2 and last 2 digits
    last_two_digits = hex_block[:2]
    first_two_digits = hex_block[-2:]
    # Convert the digits to integers
    first_decimal = int(first_two_digits, 16)
    last_decimal = int(last_two_digits, 16)
    return [first_decimal, last_decimal]
###########################################
def listOfList2String(bigList):
    result_string = []
    for sublist in bigList:
        result_string.extend(sublist)
           
    stringsave =''
    dimension = len(result_string);
    for i,idx in enumerate(result_string):
        if (i < dimension):
            stringsave+= str(idx)+" "
        else :
            stringsave+=str(idx)
    
    del(result_string)
    return stringsave.strip()
###########################################
def create_string_array(input_string):
    # Split the input string by spaces
    number_pairs = input_string.split()
    
    # Ensure that the list has an even number of elements
    if len(number_pairs) % 2 != 0:
        raise ValueError("The input string must contain an even number of numbers.")
    
    # Convert the list into pairs of strings
    string_array = [number_pairs[i]+' '+ number_pairs[i + 1] for i in range(0, len(number_pairs), 2)]
    
    return string_array
###########################################
def compare_and_add_elements(l1, l2):
    # Use a set for l2 for faster lookup
    set_l2 = set(l2)
    
    # Iterate through l1 and check if any element is not in l2
    for element in l1:
        if element not in set_l2:
            # If element is not found in l2, add it to l2
            l2.append(element)
            set_l2.add(element)  # Update the set to include the new element
    
    return l2
############################################


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" , action='store_true',help="provide the binary input file produced by PICMIC0/SAMPIC")
    parser.add_argument("PARAMS", nargs='+')
    parser.add_argument("-o", "--outDir", help="provide the output folder to save the processed ASCII data")
    args, unknown = parser.parse_known_args()
    if not sys.stdin.isatty():
        args.PARAMS.extend(sys.stdin.read().splitlines())
     
    # loading the tailed file
    for f in args.PARAMS :
        # variable defintions
        dump =1
        mat=[]
        numPixelsList = []
        allPixelsList = []
        timeStampList = []
        timeStampList2 = []
        totalEvts=0
        
        testList = []
        
        inFileName = f.split('/')[0]
        outFileName = inFileName.split('.')[0]+'.csv'
    
        # inFile
        file = open(f,"rb")
    
        ## Reading information from the file comments
        head=file.readline(); ## line1
        ##print(head,'----------------------- 1')
        infoFromComments  = str(head).split("==")[2].split("=")[1:]
        runInfo = [i.split(' ')[1] for i in infoFromComments]
    
        head=file.readline(); ## line2
        ##print(head,'----------------------- 2')
        freq = int(str(head).split("==")[-2].split(' ')[4])

        ## lines 3 
        head=file.readline() # 3 #=== DATA STRUCTURE PER FRAME===
        ##print(head,'----------------------- 3')
        newVarValues = [int(i.split(' ')[1]) for i in str(head).split(':')[2:] ]
        newVarNames = [ j.split(' ')[-1].strip() for j in str(head).split(':')[1:]]
        dictNewVars = dict(zip(newVarNames,newVarValues))

        head=file.readline() # line 4 # === NB_OF_PIXELS_IN_FRAMES (2 bytes) RAW_TIMESTAMP (in fe_clock_periods) (5 Bytes), PIXEL_COLUMN (1 byte), PIXEL ROW ( 1 byte) ==
        ##print(head,'----------------------- 4')
        head=file.readline() # line 5 #
        ##print(head,'----------------------- 5')
        head=file.readline() # line 6 #
        ##print(head,'----------------------- 6')
    
        count = 0
      
        
        
        while dump : 
            count +=1

            line=file.readline() # line 7 #
            #print(line,'----------------------- 7')
            
            if not line:
                dump = False
                break
            
            nFrames = int(str(line[:18]) .split(' ')[-2].strip())
            #print('nFrames=',nFrames)
            
            unixTime = float(str(line).split(" ")[-2])
            #print('unixTime=',unixTime)
            
            lastTime= []
            dtime = 0
            mlist0 = None
            mlistx = None
            for jdx in range(nFrames):
                #print('--> Frame=',jdx)
            
                #unixTime = float(str(line).split(" ")[-2])
                #print('unixTime=',unixTime)
        
                line=file.readline() # line 8 #
                
                #print(line,'----------------------- 8')
                timeStamp=int(str(line).split(" ")[-2])
                #print('TIME-STAMP:',timeStamp)
                lastTime.append(timeStamp) 
                
                if ( nFrames>1 ):
                    dtime=int(lastTime[jdx])-int(lastTime[jdx-1])
                    #print('DeltaTime:',dtime,', jdx',lastTime[jdx], ', jdx -1',lastTime[jdx-1], 'real jdx', jdx)
                
                #dtime = abs(timeStamp - dtime)
                nbPixels = int(str(line).split(" ")[-4])
            
                line = str(file.readline()).replace('.','')
            ##print(head,'----------------------- 9')
            
                RCs = line[2:-3].split(" ")
                mat = [hex_block_to_decimal(i) for i in RCs] 
            
                spixels = listOfList2String(mat)
                ##print(str(nbPixels),spixels)
                if (jdx == 0) :
                    mlist0 = create_string_array(spixels)
                    #print('mlist0:',mlist0)
                else :
                    mlistx = create_string_array(spixels)
                    #print('mlistx:',mlistx)
                    if (dtime<6400):
                        compare_and_add_elements(mlistx, mlist0)
                #print(result)
                #print('mlist0:',mlist0)
                #print('~ ~ ~ ~ ~ ~ ~ ~ ')
                
                ##spixels = listOfList2String(mat)
                toprint = ''
                for i in mlist0:
                    toprint=i+' '+toprint
                print(len(mlist0),toprint.strip())

                
                
            ##print('---------------------------------------------------------')
        
        file.close()
    exit()
    
##########################################    
if __name__ == "__main__":
    main()
