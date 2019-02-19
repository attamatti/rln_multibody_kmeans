#!/usr/bin/env python

# given a list pf particles get them from a data starfile.

import sys

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
	labels,header,data = read_starfile_new(sys.argv[1])
	parts_list = open(sys.argv[2],'r').readlines()
except:
	sys.exit('\nUSAGE: rln_get_particles_from_starfile.py <data star file> <parts list file>')

output = open('KMclass_{0}.star'.format(sys.argv[2].split('_')[0]),'w')
for i in header:
	output.write('{0}\n'.format(i))

parts_list = [x.replace('\n','') for x in parts_list]
n = 0

pnamedic = {}

for i in data:
    try:
	pnamedic[i[labels['_rlnImageName']]] = i
    except:
	break    

allparts = set(pnamedic.keys())
goodparts = set(parts_list)
keepers = allparts.intersection(goodparts)

print ('{0} particles'.format(len(keepers)))

for i in keepers:
	output.write('{0}\n'.format('\t'.join(pnamedic[i])))

#for i in data:
#	print i
#	try:
#		if i[labels['_rlnImageName']] in parts_list:
#			output.write('{0}\n'.format('\t'.join(i)))
#			n+=1
#	except:
#		break
#print('{0} parts'.format(n))
