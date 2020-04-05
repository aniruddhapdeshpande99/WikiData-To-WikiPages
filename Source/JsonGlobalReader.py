import json
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api
with open('../../Social_Computing/hi_monument_dump.json') as f:
	monument_list = json.load(f)

qualifiers_list, property_list, references_list, complete_final_monument_list = [], [], [], []
final_qualifiers_list, final_references_list, final_monument_list = {}, {}, {}
count_mon = 0

for monument in monument_list:
	count_mon += 1
	print(count_mon)
	if count_mon % 4 == 0: 
		print("HELLO")
		partition_num = str(count_mon / 4).split('.')[0]
		with open('../../Downloads/hi_monument_english_labels'+ partition_num + '.json', 'w') as fout:
			json.dump(complete_final_monument_list, fout)
		complete_final_monument_list = []
		print("Checkpoint %d reached, JSON dumps saved |" % (count_mon / 4))

	for key, val in monument.items():
		if key == "title":
			monument['title'] = WikidataItem(get_entity_dict_from_api(str(val))).get_label()
		elif key == "id":
			monument['id'] = WikidataItem(get_entity_dict_from_api(str(val))).get_label()

	for key in monument['claims'].keys():
		if(key == "P727"):
			continue
		else:
			property_list.append(WikidataProperty(get_entity_dict_from_api(key)).get_label())
	final_monument_list = dict(zip(property_list, list(monument['claims'].values())))
	monument['claims'].clear()
	monument['claims'].update(final_monument_list)
	property_list = []

	for key, val in monument['claims'].items():
		for values in val:
			if 'references' in values:
				for i in range(len(values['references'])):
					for key1 in values['references'][i]['snaks'].keys():
						references_list.append(WikidataProperty(get_entity_dict_from_api(key1)).get_label())
					final_references_list = dict(zip(references_list, list(values['references'][i]['snaks'].values())))
					values['references'][i]['snaks'].clear()
					values['references'][i]['snaks'].update(final_references_list)
					references_list = []
			if 'qualifiers' in values:
				for key2 in values['qualifiers'].keys():
					qualifiers_list.append(WikidataProperty(get_entity_dict_from_api(key2)).get_label()) 
				final_qualifiers_list = dict(zip(qualifiers_list, list(values['qualifiers'].values())))
				values['qualifiers'].clear()
				values['qualifiers'].update(final_qualifiers_list)
				qualifiers_list = []

			for key3, val3 in values.items():

				if key3 == "qualifiers-order":
					for i in range(len(values[key3])):
						values[key3][i] = WikidataProperty(get_entity_dict_from_api(str(values[key3][i]))).get_label()
		
				if key3 == "mainsnak":
					if(values['mainsnak']['property'] != "P727"):
						values['mainsnak']['property'] = WikidataProperty(get_entity_dict_from_api(values['mainsnak']['property'])).get_label()
					if isinstance(values['mainsnak']['datavalue']['value'], dict) and "id" in values['mainsnak']['datavalue']['value']:
						if values['mainsnak']['datavalue']['value']['id'].startswith("Q"):
							values['mainsnak']['datavalue']['value']['id'] = WikidataItem(get_entity_dict_from_api(values['mainsnak']['datavalue']['value']['id'])).get_label()
						else:
							values['mainsnak']['datavalue']['value']['id'] = WikidataProperty(get_entity_dict_from_api(values['mainsnak']['datavalue']['value']['id'])).get_label()

				if key3 == "references":
					for i in range(len(values['references'])):
						for j in range(len(values['references'][i]['snaks-order'])):
							values['references'][i]['snaks-order'][j] = WikidataProperty(get_entity_dict_from_api(values['references'][i]['snaks-order'][j])).get_label()
						for key4, val4 in values['references'][i]['snaks'].items():
							values['references'][i]['snaks'][key4][0]['property'] = WikidataProperty(get_entity_dict_from_api(values['references'][i]['snaks'][key4][0]['property'])).get_label()
							if "datavalue" in values['references'][i]['snaks'][key4][0]:
								if isinstance(values['references'][i]['snaks'][key4][0]['datavalue']['value'], dict) and "id" in values['references'][i]['snaks'][key4][0]['datavalue']['value']:
									if values['references'][i]['snaks'][key4][0]['datavalue']['value']['id'].startswith('Q'):
										#print(values['mainsnak']['datavalue']['value']['id'])
										values['references'][i]['snaks'][key4][0]['datavalue']['value']['id'] = WikidataItem(get_entity_dict_from_api(str(values['references'][i]['snaks'][key4][0]['datavalue']['value']['id']))).get_label()
									else:
										print("HELLO")
										print(monument['claims'][key])
										values['references'][i]['snaks'][key4][0]['datavalue']['value']['id'] = WikidataProperty(get_entity_dict_from_api(str(values['references'][i]['snaks'][key4][0]['datavalue']['value']['id']))).get_label()
				if key3 == "qualifiers":
					for key5, val5 in values['qualifiers'].items():
						values['qualifiers'][key5][0]['property'] = WikidataProperty(get_entity_dict_from_api(values['qualifiers'][key5][0]['property'])).get_label()
						if isinstance(values['qualifiers'][key5][0]['datavalue']['value'], dict) and "id" in values['qualifiers'][key5][0]['datavalue']['value']:
							values['qualifiers'][key5][0]['datavalue']['value']['id'] = WikidataItem(get_entity_dict_from_api(values['qualifiers'][key5][0]['datavalue']['value']['id'])).get_label()	

	complete_final_monument_list.append(monument)
