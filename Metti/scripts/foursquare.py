###### .######


##############################################################################################
# -*- coding: utf-8 -*-
# Script to read in the foursquare data
# Based on developing done by iaciac: https://github.com/MettiHoof/3circles/tree/master/iaciac
# Written by Maarten Vanhoof, may 2019
# Python 2.7
#
# Source data was downloaded from dropbox related to the future cities challengesmod/simim/blob/master/scripts/miniSIM.py

##############################################################################################


print("The script is starting")


########################################################
#0. Setup environment
########################################################

############################
#0.1 Import dependencies
############################
import pandas as pd #For data handling
import numpy as np #For matrix handling
import geopandas as gpd #For shapefile and geodatabase handling
import matplotlib.pylab as plt #For interactive plotting
from shapely.geometry import Point #For the creation of point geometries in geopandas

############################
#0.2 Setup in and output paths
############################
#Where inputdata lives and output will be put
foldername_input ='/Users/Metti_Hoof/Desktop/foursquare/data' 
foldername_output ='/Users/Metti_Hoof/Desktop/foursquare/output' 

########################################################
#1. Read in inputfiles
########################################################
############################
#1.1 Set names of inputfiles
############################

#inputfiles for movement
inputfile_movements= foldername_input + '/movements_v2/London_movements_v2.csv' 

#inputfiles for venues
inputfile_venues= foldername_input + '/venues_v2/London_venue_info_v2.csv' 

#inputfiles for category tree
#All category tree of Foursquare. Count the number of space in the begining of string to indicate the level of category. 
#Downloadeded from https://gist.github.com/tndoan/24ea389efbe137d9a514
#File is from 2015, we should get a recent one using the foursquare api:
#https://developer.foursquare.com/docs/api/venues/categories
inputfile_cattree= foldername_input + '/category_tree/4sq_category_tree.txt' 

#input shapefile for LSOA level in London
inputfile_shapefile_LSOA_LD= foldername_input+ '/LSOA_2011_London_gen_MHW/LSOA_2011_London_gen_MHW.shp'

############################
#1.2. Read in data
############################

#Read in movement csv in pandas
#df_M=pd.read_csv(inputfile_movements,sep=',')
#print '\n The first five lines of the movememts csv look like this'
#print df_M.head() 


#Read in venues csv in pandas
df_V=pd.read_csv(inputfile_venues,sep=',')
print '\n The first five lines of the venues csv look like this'
print df_V.head() 

#Read in shapefile for LSOA level in London in geopandas. 
gp_LSOA_LD=gpd.read_file(inputfile_shapefile_LSOA_LD)
#Keep only the columns that interest us.
gp_LSOA_LD = gp_LSOA_LD[['LSOA11CD','geometry']]

#print '\n The first five lines of the shapefile on LSOA in London look like this'
#print gp_LSOA_LD.head() 

#print '\n We are now plotting the extent of the LSOA in London shapefile'
#gp_LSOA_LD.plot()
#plt.show()
#plt.close('ALL')

############################
#1.2. Read in category tree
############################

#Define helper function
def getCateTree():
    f = open(inputfile_cattree, 'r')
    lines = f.readlines()
    f.close()
    result = dict()
    i = 0
    curr = None
    listOfStacks = [[] for j in range(4)]
    while i < len(lines):
        line = lines[i]
        l = line.lstrip(' ')
        if l.startswith('Suggested Countries:'):
            i = i + 1
            continue
        space = len(line) - len(line.lstrip(' '))
        loc = space / 4
        if curr != None:
            if curr <= loc: # it move to right, subcategory
                listOfStacks[loc].append(l.strip('\n'))
            else: # it moves to left, end of subcategory
                index = len(listOfStacks[loc]) - 1 # the last element of stack
                for name in listOfStacks[curr]:
                    result[name] = listOfStacks[loc][index]
                listOfStacks[curr] = []
        i = i + 1
        curr = loc
        listOfStacks[loc].append(l.strip('\n'))
    return result

#get a dict with all the categories.
dict_cattree = getCateTree()


########################################################
#2. Organise the venues data by categorie
########################################################

############################
#2.1 Get an insight on the  different categories and the amounts of time they occur in the venues data
############################

#put reset index because value counts gives you a series and you'd prefer a datframe.
df_V_category_count=df_V['category'].value_counts(sort=True).reset_index()
df_V_category_count.columns=['category','count']

print '\n The amount a category occurs in the venue dataset is:'
print df_V_category_count

#filter on categories that occur at least x times.
x=50
df_V_category_count_minx=df_V_category_count[df_V_category_count['count']> x]

print '\n The categories that occur more than x time in the dataset are:'
print df_V_category_count_minx


############################
#2.2 Identify the higher categories of the data using the category tree
############################

def category_up(row):
	#Not all categories are in the dict_cattree. If they are not in the cattree, we keep their names
	if row['category'] in dict_cattree.keys():
		text=row['category']
		text2=text[:-1]
		up=dict_cattree[row['category']]

	#In a lot of cases, the tree says cafe whereas the data says cafes. so we omit the s
	elif row['category'][:-1] in dict_cattree.keys():
		up=dict_cattree[row['category'][:-1]]
		#up='This was a case with one letter differences, an s '
	else:
		#up=row['category']
		up='NaN'
	#print up 
	return up


def category_up_up(row):
	#Not all categories are in the dict_cattree. If they are not in the cattree, we keep their names
	if row['category_up'] in dict_cattree.keys():
		text=row['category_up']
		text2=text[:-1]
		up_up=dict_cattree[row['category_up']]

	#In a lot of cases, the tree says cafe whereas the data says cafes. so we omit the s
	elif row['category_up'][:-1] in dict_cattree.keys():
		up_up=dict_cattree[row['category_up'][:-1]]
		#up='This was a case with one letter differences, an s '
	else:
		#up=row['category']
		up_up=row['category_up']
	#print up 
	return up_up

def category_up_up_up(row):
	#Not all categories are in the dict_cattree. If they are not in the cattree, we keep their names
	if row['category_up_up'] in dict_cattree.keys():
		text=row['category_up_up']
		text2=text[:-1]
		up_up_up=dict_cattree[row['category_up_up']]

	#In a lot of cases, the tree says cafe whereas the data says cafes. so we omit the s
	elif row['category_up_up'][:-1] in dict_cattree.keys():
		up_up_up=dict_cattree[row['category_up_up'][:-1]]
		#up='This was a case with one letter differences, an s '
	else:
		#up=row['category']
		up_up_up=row['category_up_up']
	#print up 
	return up_up_up

#Apply the up, up_up and up_up_up categories
df_V['category_up'] = df_V.apply(category_up, axis=1)
df_V['category_up_up'] = df_V.apply(category_up_up, axis=1)
df_V['category_up_up_up'] = df_V.apply(category_up_up_up, axis=1)
print df_V.head()

#Have a look at occurences - note that 3991 out of 22689 venues 
#were not categorized at a higher level, that is 17% of the dataset 

#df_V['category_up'].value_counts(sort=True)
#df_V['category_up_up'].value_counts(sort=True)
#df_V['category_up_up_up'].value_counts(sort=True)


########################################################
#3. Map venues data by category
########################################################


############################
#3.1 Transfer venues dataset from pandas to geopandas
############################

#Transfer data to plot to geopandas, creating a point geometry entry based on the lon lat coordinates.
gp_V= gpd.GeoDataFrame(df_V.drop(['lat', 'lng'], axis=1),
                                 crs={'init': 'epsg:4326'},
                                 geometry=[Point(x, y) for x, y in zip(df_V.lng, df_V.lat)])

print '\n The first five lines of the venues dataset in geopandas look like this:'
print gp_V.head()

gp_LSOA_LD

#Set projection from shapefile and geopandas to be the same.
gp_LSOA_LD = gp_LSOA_LD.to_crs({'proj': 'tmerc'})
gp_V = gp_V.to_crs({'proj': 'tmerc'})


############################
#3.2 Plot map for one specified category at one specified category_level
############################

category_level='category' #'category','category_up','category_up_up','category_up_up_up'
category_to_plot='Pubs'

#define outputfile name and location at which the map will be saved
#we called this folder individual
outputfile= foldername_output + '/individual/map_venues_category_%s_at_level_%s.png' %(category_to_plot,category_level)

#Select data for category to plot
gp_V_to_plot=gp_V[gp_V[category_level]==category_to_plot]


#plot gp_V_to_plot
f, ax = plt.subplots(1, figsize=(10., 8.), dpi=200, subplot_kw=dict(aspect='equal'))
ax.axis('off')

gp_LSOA_LD.plot(ax=ax, linewidth=0.05, facecolor='#D5E3D8', edgecolor='#111111', alpha=0.8)
gp_V_to_plot.plot(ax=ax, linewidth=0.1, facecolor='#AE4B16', alpha=0.9, edgecolor='#AE4B16', markersize=2)

title_text= 'Locations of venues for category %s at level: %s ' %(category_to_plot,category_level)
plt.title(title_text)

#plt.tight_layout()
#plt.show()
#plt.close('ALL')
plt.savefig(outputfile, dpi=200, transparent=True, tight_layout=True)
#Clear the current figure so we don't take upt too much memory
plt.clf()
#Close all open pylab windows
plt.close('ALL')


############################
#3.3 Plot map for all categories at one specified categorylevel
############################

category_level='category_up_up_up' #'category','category_up','category_up_up','category_up_up_up'

#helperfunction to define n distinct colors 
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)
# setup color scheme and color counter
cmap = get_cmap(len(gp_V[category_level].unique()))
color_counter=0


for item in gp_V[category_level].unique():
	category_to_plot=item

	print 'We are now plotting for the category %s at the level of %s ' %(category_to_plot,category_level)

	#define outputfile name and location at which the map will be saved
	#folders are called based on category level
	outputfile= foldername_output + '/%s/map_venues_category_%s.png' %(category_level,category_to_plot)

	#Select data for category to plot
	gp_V_to_plot=gp_V[gp_V[category_level]==category_to_plot]

	#plot gp_V_to_plot
	f, ax = plt.subplots(1, figsize=(10., 8.), dpi=200, subplot_kw=dict(aspect='equal'))
	ax.axis('off')

	gp_LSOA_LD.plot(ax=ax, linewidth=0.05, facecolor='#D5E3D8', edgecolor='#111111', alpha=0.8) 
	gp_V_to_plot.plot(ax=ax, linewidth=0.1, facecolor=cmap(color_counter), edgecolor='#AE4B16', markersize=2)

	title_text= 'Locations of venues for category %s at level: %s ' %(category_to_plot,category_level)
	plt.title(title_text)

	#plt.tight_layout()
	#plt.show()
	#plt.close('ALL')
	plt.savefig(outputfile, dpi=200, transparent=True, tight_layout=True)
	#Clear the current figure so we don't take upt too much memory
	plt.clf()

	color_counter=color_counter+1



