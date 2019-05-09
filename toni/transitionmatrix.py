import sys

import matplotlib.pyplot as plt
import numpy as np
from math import *
#from numarray import *
#import numarray.linear_algebra as la
import copy
import random
from math import sqrt,exp,log
import operator

################################################################################################

####################################################
##Save categories trees at the up-up-up level
###########

#get a dict with all the categories.
categ={}
fh=open('/home/antonia/workspace/UCL/4squares/Data/category_tree/4sq_category_tree.txt','r')
igot = fh.readlines()
upupup=['Arts & Entertainment','College & University','Event','Food','Nightlife Spot','Outdoors & Recreation','Professional & Other Places','Residence','Shop & Service','Travel & Transport']
print 'upupup', len(upupup)
ii=0
cat=upupup[ii]
for line in igot:
	about = line.strip()
	#print about
	if about in upupup:
		ii=upupup.index(about)
		cat=cat=upupup[ii]
	#if about in categ.keys():
	#	print 'rep', about
	categ[about]=cat
print 'cat values', len(list(set(categ.values()))), 'keys',len(list(set(categ.keys()))), len(categ.keys()), len(igot)
print 'cat of Rock Club:', categ['Rock Club']
fh.close()


####################################################
## save venues id and categories
############
venues={}
fh=open('/home/antonia/workspace/UCL/4squares/Data/venues_v2/London_venue_info_v2.csv','r')
igot = fh.readlines()
del igot[0]
diff=[] #number of unlabeled categories
for line in igot:
	about = line.strip().split(',')
	vencat=about[len(about)-1]	#venue category
	try:
		cat=categ[vencat]
	except KeyError:
		try:
			#accounting for a possible final s
			cat=categ[vencat[:len(vencat)-1]]
		except KeyError:
			#if it is not in the 10upupup categories, we save it with its own name (with 'other')
			cat='other'
			#vencat
			diff.append('cat')
		
			pass
	venues[about[0]]=cat
print 'diff', len(diff), 'tot',len(igot), 'how many', len(list(set(diff)))
#thera are 101 unlabeled categories, total 2173 unlabeled venues
#print list(set(diff))
fh.close()
dims=len(set(list(categ.values())))+1
####################################################
## new read the movements between venues categories (now averything is aggregated, tomorrow I will plot more figures)
###############
fh=open('/home/antonia/workspace/UCL/4squares/Data/movements_v2/London_movements_v2.csv','r')	
igot = fh.readlines()
#we sabe all the information in here in case we need it later
transcat={}
#this is just for matplotlib:
axis=list(set(categ.values()))+['other']
print axis,'axis', dims
matrix=np.zeros((dims,dims))
for line in igot:
	about = line.strip().split(',')
	a=about[4]
	i1=axis.index(venues[about[0]])
	i2=axis.index(venues[about[1]])
	matrix[i1,i2]=matrix[i1,i2]+float(a.replace('"',''))
	try:
		transcat[(venues[about[0]],venues[about[1]])]=transcat[(venues[about[0]],venues[about[1]])]+float(a.replace('"',''))

	except KeyError:
		transcat[(venues[about[0]],venues[about[1]])]=float(a.replace('"',''))

		pass
sorted_transcat = sorted(transcat.items(), key=operator.itemgetter(1),reverse=True)
print sorted_transcat

fh.close()

plt.matshow(matrix)

plt.show()
