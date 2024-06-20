#!/usr/bin/python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import math
import random
import time
import sys

counter = sys.argv[-1]

def generate_random_numbers(n):
    random_numbers = [random.randint(-2, 2) for _ in range(n)]
    return random_numbers

def count_true_false(lst):
    true_count = lst.count(True)
    false_count = lst.count(False)
    return true_count, false_count

def distance(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return math.sqrt( math.pow(x2-x1,2) + math.pow(y2-y1,2))

tcolor = ['red','blue','gold','green','magenta','black','orange','tan','peru','cyan','pink','olive','purple','brown','lime','grey']  
mymarker = ['X','o','s','h','H','D','d','1','3','4','8','+', 'v', '^', '<', '>', 'p', '*', 'P','x','|','_','2','.']

color_marker = []
for i in mymarker :
    for j in tcolor :
        color_marker.append([j,i])


data = pd.read_csv("xlines.csv",delimiter=";")

ifile= 'inter.csv'
cfile='clusters.csv'
#cdfile = 'centroid.csv'
mypathI= os.path.isfile(ifile)
mypathC= os.path.isfile(cfile)
#mypathCD= os.path.isfile(cdfile)

print(mypathI)
print(mypathC)
#print(mypathCD)


if (mypathI):
    df= pd.read_csv(ifile, delimiter=";")

if (mypathC):
    df_clus = pd.read_csv(cfile,delimiter=';')
    
##if (mypathCD):
##    df_cd = pd.read_csv(cdfile,delimiter=';')

for idx in range(data.index.stop) :
    color='black'
    way=data.track[idx]
    
    if way[0]=='B' :
        tcolor='blue'
    elif way[0]=='R':
        tcolor='red'
    elif way[0]=='Y':
        tcolor='gold'
        
    line0 = (eval(data.pt0[idx]),eval(data.pt1[idx]))
    xs,ys = zip(*line0)
    plt.plot(xs,ys,'--', markersize=0, color=tcolor, linewidth=.3)


if (mypathI):
    
    dim = df.index.stop
    fillCounter = -1
    count = 0 
    
    for i in range(dim):
        px = df.x[i]
        py  = df.y[i]
        plt.scatter(px,py,2,color='black',marker='x')
        ##plt.text(px+generate_random_numbers(1), py+generate_random_numbers(1), str(i), fontsize=8, ha='right', va='bottom')

plt.xlabel('X-axis [$\mu$m]')
plt.ylabel('Y-axis [$\mu$m]')
plt.savefig('lines_evt'+str(counter)+'.png')
#plt.show()
plt.figure()

if (mypathC) :
    dimClus = df_clus.index.stop
    ##dimCD = df_cd.index.stop
    
    print( df_clus.x.min() )
    print( df_clus.x.max() )
    
    for idx in range(dimClus):
        nclus = df_clus.clusNumber[idx]
        xclus = df_clus.x[idx]
        yclus= df_clus.y[idx]
        plt.scatter(xclus,yclus,facecolors='none',s=20,color=color_marker[nclus][0],marker=color_marker[nclus][1])
        plt.xlim(df_clus.x.min()-10,df_clus.x.max()+10 )
        plt.ylim(df_clus.y.min()-10,df_clus.y.max()+10 )
        
    for idx in range(data.index.stop) :
        color='black'
        way=data.track[idx]

        line0 = (eval(data.pt0[idx]),eval(data.pt1[idx]))
        xs,ys = zip(*line0)
        plt.plot(xs,ys,'--', markersize=0, color='black', linewidth=.3)
        plt.xlabel('X-axis [$\mu$m]')
        plt.ylabel('Y-axis [$\mu$m]')
        plt.title('PICMIC$0$ Intersections, Centroids and Re-Clusterization -- #inter:'+str(i))
        plt.grid()
        
        
    ##for jdx in range(dimCD):
    ##    this_x = df_cd.x[jdx]
    ##    this_y = df_cd.y[jdx]
    ##    plt.scatter(this_x,this_y,facecolors='none',s=40,color=color_marker[nclus][0],marker='D', label='('+str(this_x)+','+str(this_y)+')'+'[$\mu$m]')
        
    ##plt.legend()
    #plt.savefig('clustering_evt'+str(counter)+'.png')
    plt.show()    
exit()
