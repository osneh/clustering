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
        infoFromComments  = str(head).split("==")[2].split("=")[1:]
        runInfo = [i.split(' ')[1] for i in infoFromComments]
    
        head=file.readline(); ## line2
        freq = int(str(head).split("==")[-2].split(' ')[4])

        ## lines 3 
        head=file.readline() # 3 #=== DATA STRUCTURE PER FRAME===
        newVarValues = [int(i.split(' ')[1]) for i in str(head).split(':')[2:] ]
        newVarNames = [ j.split(' ')[-1].strip() for j in str(head).split(':')[1:]]
        dictNewVars = dict(zip(newVarNames,newVarValues))

        head=file.readline() # line 4 # === NB_OF_PIXELS_IN_FRAMES (2 bytes) RAW_TIMESTAMP (in fe_clock_periods) (5 Bytes), PIXEL_COLUMN (1 byte), PIXEL ROW ( 1 byte) ==
        head=file.readline() # line 5 #
        head=file.readline() # line 6 #
    
        count = 0
        
        while dump : 
            count +=1

            line=file.readline() # line 7 #
            
            if not line:
                dump = False
                break
            
            unixTime = float(str(line).split(" ")[-2])
        
            line=file.readline() # line 8 #
            timeStamp=int(str(line).split(" ")[-2])
            nbPixels = int(str(line).split(" ")[-4])
            
            line = str(file.readline()).replace('.','')
            
            RCs = line[2:-3].split(" ")
            mat = [hex_block_to_decimal(i) for i in RCs] 
            
            spixels = listOfList2String(mat)
            print(str(nbPixels),spixels)
        
        file.close()
    exit()
    
##########################################    
if __name__ == "__main__":
    main()
