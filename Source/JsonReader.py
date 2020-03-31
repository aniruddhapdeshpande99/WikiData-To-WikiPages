import json
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api
with open('../../Downloads/en_monument_dump_part1.json') as f:
	monument_list = json.load(f)

qualifiers_list, property_list, references_list = [], [], []
final_qualifiers_list, final_references_list, final_monument_list = {}, {}, {}

for monument in monument_list:
	for key, val in monument_list[9].items():
		if key == "title":
			monument['title'] = WikidataItem(get_entity_dict_from_api(str(val))).get_label()
		elif key == "id":
			monument['id'] = WikidataItem(get_entity_dict_from_api(str(val))).get_label()

for monument in monument_list:
	for key in monument['claims'].keys():
		property_list.append(WikidataProperty(get_entity_dict_from_api(key)).get_label())
	final_monument_list = dict(zip(property_list, list(monument['claims'].values())))
	monument['claims'].clear()
	monument['claims'].update(final_monument_list)
	property_list = []

for monument in monument_list:	
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

for monument in monument_list:
	for key, val in monument['claims'].items():
		for values in val:
			for key1, val1 in values.items():

				if key1 == "qualifiers-order":
					for i in range(len(values[key1])):
						values[key1][i] = WikidataProperty(get_entity_dict_from_api(str(values[key1][i]))).get_label()
		
				if key1 == "mainsnak":
					values['mainsnak']['property'] = WikidataProperty(get_entity_dict_from_api(values['mainsnak']['property'])).get_label()
					if isinstance(values['mainsnak']['datavalue']['value'], dict) and "id" in values['mainsnak']['datavalue']['value']:
						values['mainsnak']['datavalue']['value']['id'] = WikidataItem(get_entity_dict_from_api(values['mainsnak']['datavalue']['value']['id'])).get_label()
		
				if key1 == "references":
					for i in range(len(values['references'])):
						for j in range(len(values['references'][i]['snaks-order'])):
							values['references'][i]['snaks-order'][j] = WikidataProperty(get_entity_dict_from_api(values['references'][i]['snaks-order'][j])).get_label()
						for key2, val2 in values['references'][i]['snaks'].items():
							for k in range(len(values['references'][i]['snaks'][key2])):
								values['references'][i]['snaks'][key2][k]['property'] = WikidataProperty(get_entity_dict_from_api(values['references'][i]['snaks'][key2][k]['property'])).get_label()
								if isinstance(values['references'][i]['snaks'][key2][k]['datavalue']['value'], dict) and "id" in values['references'][i]['snaks'][key2][k]['datavalue']['value']:
									values['references'][i]['snaks'][key2][k]['datavalue']['value']['id'] = WikidataItem(get_entity_dict_from_api(str(values['references'][i]['snaks'][key2][k]['datavalue']['value']['id']))).get_label()

				if key1 == "qualifiers":
					for key3, val3 in values['qualifiers'].items():
						values['qualifiers'][key3][0]['property'] = WikidataProperty(get_entity_dict_from_api(values['qualifiers'][key3][0]['property'])).get_label()
						if isinstance(values['qualifiers'][key3][0]['datavalue']['value'], dict) and "id" in values['qualifiers'][key3][0]['datavalue']['value']:
							values['qualifiers'][key3][0]['datavalue']['value']['id'] = WikidataItem(get_entity_dict_from_api(values['qualifiers'][key3][0]['datavalue']['value']['id'])).get_label()

'''for monument in monument_list:
	for key, val in monument['claims'].items():
		print(key, val)
		print("\n")
	print("\n\n")'''