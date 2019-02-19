#!/usr/bin/env python

from scipy.cluster.vq import whiten,kmeans
import numpy as np
import matplotlib.pyplot as plt
import math
import sys

try:
    infile = open(sys.argv[1],'r').readlines()
    nclasses = int(sys.argv[2])
    neigens = int(sys.argv[3])
except:
    sys.exit('USAGE: rln_multibody_kmeans.py <input file> <n classe> <n eigenvectors>')
    
#get the data from the relion text file output

reliondata = []
dataids = []
for i in infile:
    line = i.split()
    dataids.append(line[0])
    reliondata.append(line[1:neigens+1])
reliondata = np.array(reliondata,dtype='float32')
white_data = whiten(reliondata)
codebook,distortion = kmeans(white_data,nclasses)

#make datadic
datadic = {}
n=0
for i in dataids:
    datadic[i] = reliondata[n]
    n+=1


def distance_between(point1,point2):
    difs = []
    sublists = zip(point1,point2)
    for i in sublists:        
        difs.append(abs(i[0]-i[1]))
    return(np.sum(difs))

#organise that data into classes
dataclusters = {}
datan=0
for datapoint in white_data:
    clustn = 0
    cmin =10000
    for clust in codebook:
        #print (dataids[datan],clustn,distance_between(datapoint,clust))
        clustdist = distance_between(datapoint,clust)
        if clustdist < cmin:
            cmin = clustdist
            cluster = clustn
        clustn+=1
    try:
        dataclusters[cluster].append(dataids[datan])
    except:
        dataclusters[cluster] = [dataids[datan]]
    datan+=1

#write an output file for each class:
for i in dataclusters:
    output = open('{0}_parts_out.txt'.format(i),'w')
    for j in dataclusters[i]:
        output.write('{0}\n'.format(j))
    output.close()

#scatterplots
empty = []
for i in range(0,nclasses):
    empty.append([])
    
        
    
statsdic = dict(zip(range(0,nclasses),empty))               #{classno:[[eigenvals1],[eigenvals2],...,[eigenvalsn]]} - for doing statistics
first = True
for x in range(0,len(reliondata[0])):    
    for i in dataclusters:
        datax = []
        datay = []
        #print i, dataclusters[i]
        for j in dataclusters[i]:
            datax.append(i)
            datay.append(datadic[j][x])
        statsdic[i].append(datay)
       
        plt.scatter(datax,datay,s=10)
        ##don't know if these lines add anything...
        #liney = (np.mean(datay)+np.std(datay),np.mean(datay)-np.std(datay))
        #linex = (datax[0],datax[0])
        #plt.plot(linex,liney)
    plt.xticks(range(0,nclasses))
    plt.xlabel('class')
    plt.ylabel('eigen value')
    plt.title('eigen vector {0}'.format(x))
    plt.savefig('plt{0}.png'.format(x))
    plt.close()

# do the statistics
for i in statsdic:
    n=1
    print('class {0} -- {1} particles'.format(i,len(statsdic[i][0])))
    print('PC\tmean\tstd')
    for j in statsdic[i]:
        print('{0}\t{1}\t{2}'.format(n,round(np.mean(j),2),round(np.std(j),2)))
        n+=1
    print('\n')

# make a comparison graph


for i in statsdic:
    colors = ['red','blue','green','yellow','black','orange']
    cn =0
    offset = 0
    for j in statsdic[i]:
        plt.scatter(i+offset,np.mean(j),color=colors[cn])
        liney = (np.mean(j)+np.std(j),np.mean(j)-np.std(j))
        linex = (i+offset,i+offset)
        plt.plot(linex,liney,color=colors[cn])
        cn+=1
        offset+=0.1
vlines = [x+0.9 for x in range(0,len(statsdic))]
for i in vlines:
    plt.axvline(x=i,color='gainsboro', linestyle='--')
plt.savefig('final.png')
plt.close()