#!/usr/bin/env python

import sys

try:
	eigenvalsfile = open(sys.argv[1],'r').readlines()
	sepval = int(sys.argv[2])
	svmin = float(sys.argv[3])
	svmax = float(sys.argv[4])
except:
	sys.exit('USAGE: get_parts_eby_eigen.py <eigenvalues file> <component> <min> <max>')
	
partevdic = {}
for i in eigenvalsfile:
	line = i.split()
	partevdic[line[0]] = line[1:]

output = open('selected_particles_PC{0}_{1}_to_{2}.txt'.format(sepval,svmin,svmax),'w')

for i in partevdic:
	print float(partevdic[i][sepval])
	if float(partevdic[i][sepval]) >= svmin and float(partevdic[i][sepval]) <= svmax:
		output.write('\n{0}'.format(i))
