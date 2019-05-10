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
fh=open('/home/antonia/workspace/UCL/4squares/Data/category_tree/new4sq_category_tree.txt','r')
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
			cat='Other'
			#'other'
			#vencat
			diff.append(cat)
		
			pass
	venues[about[0]]=cat
print 'diff', len(diff), 'tot',len(igot), 'how many', len(list(set(diff)))
#thera are 101 unlabeled categories, total 2173 unlabeled venues
#print list(set(diff))
fh.close()
dims=len(set(list(categ.values())))+1

'''
##################################################################################################################
## new read the movements between venues categories London All
###############
fh=open('/home/antonia/workspace/UCL/4squares/Data/movements_v2/London_movements_v2.csv','r')	
igot = fh.readlines()
#we sabe all the information in here in case we need it later
transcat={}
#this is just for matplotlib:
axis=list(set(categ.values()))+['Other']
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
#######
## Figure
#######

fig, ax = plt.subplots()
im = ax.imshow(matrix)


# We want to show all ticks...
ax.set_xticks(np.arange(len(axis)))
ax.set_yticks(np.arange(len(axis)))
# ... and label them with the respective list entries
ax.set_xticklabels(axis)
ax.set_yticklabels(axis)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
#for i in range(len(axis)):
#    for j in range(len(axis)):
#        text = ax.text(j, i, matrix[i, j],
#                       ha="center", va="center", color="w")

ax.set_title("Transition London All")
fig.tight_layout()
fig.colorbar(im)
fig.savefig('TransitionFig/London_all.svg', dpi=fig.dpi)
fig.savefig('TransitionFig/London_all.png', dpi=fig.dpi)
plt.show()


##################################################################################################################
## new read the movements between venues categories London at different day times
###############
daytime=['"MORNING"','"MIDDAY"','"AFTERNOON"','"NIGHT"','"OVERNIGHT"']
names=['Morning','Midday','Afternoon','Night','Overnight']
for ii in range(len(daytime)):
	fh=open('/home/antonia/workspace/UCL/4squares/Data/movements_v2/London_movements_v2.csv','r')	
	igot = fh.readlines()
	#we sabe all the information in here in case we need it later
	transcat={}
	#this is just for matplotlib:
	axis=list(set(categ.values()))+['Other']
	print axis,'axis', dims
	matrix=np.zeros((dims,dims))
	for line in igot:
		about = line.strip().split(',')
		#print about[3], daytime[0]
		if about[3]==daytime[ii]:
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
	#######
	## Figure
	#######

	fig, ax = plt.subplots()
	im = ax.imshow(matrix)


	# We want to show all ticks...
	ax.set_xticks(np.arange(len(axis)))
	ax.set_yticks(np.arange(len(axis)))
	# ... and label them with the respective list entries
	ax.set_xticklabels(axis)
	ax.set_yticklabels(axis)

	# Rotate the tick labels and set their alignment.
	plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
		 rotation_mode="anchor")

	# Loop over data dimensions and create text annotations.
	#for i in range(len(axis)):
	#    for j in range(len(axis)):
	#        text = ax.text(j, i, matrix[i, j],
	#                       ha="center", va="center", color="w")

	ax.set_title('Transition London '+str(names[ii]))
	fig.tight_layout()
	fig.colorbar(im)
	fig.savefig('TransitionFig/London_'+str(names[ii])+'.svg', dpi=fig.dpi)
	fig.savefig('TransitionFig/London_'+str(names[ii])+'.png', dpi=fig.dpi)
	plt.show()

'''
##################################################################################################################
## new read the movements between venues categories London All for the different seassions 
###############
fh=open('/home/antonia/workspace/UCL/4squares/Data/movements_v2/London_movements_v2.csv','r')	
igot = fh.readlines()
seasons=[['12','01','02'],['03','04','05'],['06','07','08'],['09','10','11']]
names=['Winter','Spring','Summer','Autumn']
#we sabe all the information in here in case we need it later
for ii in range(len(seasons)):
	transcat={}
	#this is just for matplotlib:
	axis=list(set(categ.values()))+['Other']
	print axis,'axis', dims
	matrix=np.zeros((dims,dims))
	tot=0
	for line in igot:
		about = line.strip().split(',')
		a=about[4]
		b=about[2]
		time1=b.replace('"','')
		time=time1.strip().split('-')
		if time[1] in seasons[ii]:
			i1=axis.index(venues[about[0]])
			i2=axis.index(venues[about[1]])
			matrix[i1,i2]=matrix[i1,i2]+float(a.replace('"',''))
			tot=tot+1
			try:
				transcat[(venues[about[0]],venues[about[1]])]=transcat[(venues[about[0]],venues[about[1]])]+float(a.replace('"',''))

			except KeyError:
				transcat[(venues[about[0]],venues[about[1]])]=float(a.replace('"',''))

				pass
	sorted_transcat = sorted(transcat.items(), key=operator.itemgetter(1),reverse=True)
	print 'tot',tot
	fh.close()

	#######
	## Figure
	#######

	fig, ax = plt.subplots()
	im = ax.imshow(matrix)


	# We want to show all ticks...
	ax.set_xticks(np.arange(len(axis)))
	ax.set_yticks(np.arange(len(axis)))
	# ... and label them with the respective list entries
	ax.set_xticklabels(axis)
	ax.set_yticklabels(axis)

	# Rotate the tick labels and set their alignment.
	plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
		 rotation_mode="anchor")

	# Loop over data dimensions and create text annotations.
	#for i in range(len(axis)):
	#    for j in range(len(axis)):
	#        text = ax.text(j, i, matrix[i, j],
	#                       ha="center", va="center", color="w")

	ax.set_title('Transition London '+str(names[ii]))
	fig.tight_layout()
	fig.colorbar(im)
	fig.savefig('TransitionFig/London_'+str(names[ii])+'.svg', dpi=fig.dpi)
	fig.savefig('TransitionFig/London_'+str(names[ii])+'.png', dpi=fig.dpi)
	plt.show()



