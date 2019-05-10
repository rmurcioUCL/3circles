
#Juste donwloaded this cattree from the api. 
inputfile_cattree_json= foldername_input + '/category_tree/4sq_categories.json'

with open(inputfile_cattree_json, 'r') as f:
	dict_cattree_json = json.load(f)

#explore structure of dict_cattree_json

list_of_categories=dict_cattree_json['response']['categories']
#len(list_of_categories)
#list_of_categories[1].keys() #[u'pluralName', u'name', u'shortName', u'id', u'categories', u'icon']

level1=[]
level2=[]
level3=[]

dict_master_cattree={}

for dict_level1 in list_of_categories:
	#print type (dict_level1) #all dicts
	#print list_of_ten_dicts[dict_level1].keys() #[u'pluralName', u'name', u'shortName', u'id', u'categories', u'icon']
	print dict_level1['name']
	level1.append(dict_level1['name'])

	list_of_categories_from_level1=dict_level1['categories']

	for dict_level2 in list_of_categories_from_level1:
		print "\t" + dict_level2['name']
		level2.append(dict_level2['name'])
		dict_master_cattree[dict_level2['name']]=dict_level1['name']

		list_of_categories_from_level2=dict_level2['categories']

		for dict_level3 in list_of_categories_from_level2:
			print "\t\t" + dict_level3['name']
			level3.append(dict_level3['name'])
			dict_master_cattree[dict_level3['name']]=dict_level2['name']