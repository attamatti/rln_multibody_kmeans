#!/usr/bin/env python

import sys
import numpy as np

try:
	partslist = open(sys.argv[1],'r').readlines()
	evslist = open(sys.argv[2],'r').readlines()
except:
	sys.exit('\nUSAGE: get_eigens_stats_from_class.py <parts_out file> <relion eigenvaluse file>')
evsdic = {}
for i in evslist:
	split = i.split()
	evsdic[split[0]] = split[1:]

vals = []
for i in partslist:
	vals.append(evsdic[i.replace('\n','')])


sortedvals = vals[0]
count = len(vals[0])

for i in range(count):
	sum1 = [float(x[i]) for x in vals]
	mean = np.mean(sum1)
	stdev = np.std(sum1)
	print i	
	print len(sum1)
	print mean
	print stdev

