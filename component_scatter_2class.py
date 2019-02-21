#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
import random

def getvals(parts,evs,ev1,ev2):
	try:
		partslist = open(parts,'r').readlines()
		evslist = open(evs,'r').readlines()
	except:
		sys.exit('\nUSAGE: get_eigens_stats_from_class.py <component#> <component #> <relion eigenvaluse file> <parts_out file>')
	evsdic = {}
	for i in evslist:
		split = i.split()
		evsdic[split[0]] = split[1:]

	vals = []
	for i in partslist:
		try:
			vals.append(evsdic[i.replace('\n','')])
		except:
			print i
	sortedvals = vals[0]
	count = len(vals[0])

	sum1 = [float(x[int(ev1)]) for x in vals]
	sum2 = [float(x[int(ev2)]) for x in vals]
	
	mean1 = np.mean(sum1)
	stdev1 = np.std(sum1)
	
	mean2 = np.mean(sum2)
	stdev2 = np.std(sum2)
	n = len(sum1)
	return (sum1,sum2,mean1,stdev1,mean2,stdev2,n)

ev1,ev2 = sys.argv[1:3]
for i in sys.argv[4:]:
	color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
	print color
	clno = i.split('_')[0]	
	x,y,mx,sx,my,sy,count = getvals(i,sys.argv[3],ev1,ev2)
	linex = [mx-sx,mx+sx]
	lx2 = [my,my]
	liney = [my-sy,my+sy]
	ly2 = [mx,mx]
	plt.scatter(mx,my,color=color,s=(count/500))
	plt.plot(linex,lx2,color=color)
	plt.plot(ly2,liney,color=color)
	plt.xlabel('component {0}'.format(ev1))
	plt.ylabel('component {0}'.format(ev2))
	plt.tight_layout()
plt.savefig('{0}v{1}.png'.format(ev1,ev2))
