#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile_new(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i:
            labelsdic[i.split()[0]] = labcount
            labcount +=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        elif len(i.split())>=1:
            data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#

try:
	partslist = open(sys.argv[1],'r').readlines()
	evslist = open(sys.argv[2],'r').readlines()
except:
	sys.exit('\nUSAGE: get_eigens_stats_from_class.py <parts_out file or starfile> <relion eigenvaluse file>')
evsdic = {}
for i in evslist:
	split = i.split()
	evsdic[split[0]] = split[1:]

vals = []
if sys.argv[1].split('.')[-1] == 'txt':
	for i in partslist:
		vals.append(evsdic[i.replace('\n','')])
elif sys.argv[1].split('.')[-1] == 'star':
	labels,header,data = read_starfile_new(sys.argv[1])
	for i in data:
		vals.append(evsdic[i[labels['_rlnImageName']]])

sortedvals = vals[0]
count = len(vals[0])




for i in range(count):
	sum1 = [float(x[i]) for x in vals]
	mean = np.mean(sum1)
	stdev = np.std(sum1)
	plt.scatter(i,mean)
	linex = [i,i]
	liney = [mean+stdev,mean-stdev]
	plt.plot(linex,liney)
	plt.xlabel('principal component')
	plt.title('{0}'.format(sys.argv[1].split('.')[0]))
	plt.ylabel('eigenvalue')
	plt.savefig('EC_{0}.png'.format(sys.argv[1].split('.')[0]))
	print('principal component',i)	
	print('mean',mean)
	print('stdev',stdev)
print('#particles',len(vals))

