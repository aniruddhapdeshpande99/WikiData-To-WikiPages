#!/usr/bin/env python
# coding: utf-8

# #### 1. Importing Libraries

# In[3]:


import json
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api
import json
import time
from googletrans import Translator


# #### 2. Reading Monument List

# In[4]:


monument_list = []
translations_count = 0

with open('../Data/Wikidata_JSON/hi_monument_dump.json') as f:
    new_list = json.load(f)
    monument_list = monument_list + new_list


# #### 3. Retrieving Labels for Property Value pairs for each monument

# In[3]:


def str_translator(string_text):
    if translations_count%2 == 0:
        time.sleep(2)
    
    elif translations_count%10 == 0:
        time.sleep(15)
    
    translator = Translator()
    translations_count += 1
    return translator.translate(string_text, dest='hi').text

def extract_dict_hindi_labels(value_dictionary):
    hi_dict_keys = {}
    for key in value_dictionary.keys():
        hi_dict_keys[key] = str_translator(key)
    hi_value_dictionary = {}
    for key in value_dictionary.keys():
        hi_value_dictionary[hi_dict_keys[key]] = str_translator(str(value_dictionary[key]))
    return hi_value_dictionary


# In[4]:


labelled_monument_list = {}
label_list = {}
non_labelled_props = ['P727']

t0 = time.time()

count_monuments = 0

for monument in monument_list:
    
    monument_labelled_prop_val = {}
    list_prop_value = monument['claims']
    list_properties = list(list_prop_value.keys())
    
    #Removing Properties from list of properties which dont have a wikidata page
    for prop in non_labelled_props:
        if prop in list_properties:
            list_properties.remove(prop)
    
    list_properties_copy = list_properties
    
    #Adding all properties to label list. The ones which dont have wikidata pages are stored in non_labelled_props 
    for prop in list_properties:
        if prop not in label_list.keys():
            try:
                prop_details = get_entity_dict_from_api(prop)
                if 'hi' in prop_details['labels'].keys():
                    prop_label = prop_details['labels']['hi']['value']
                else:
                    prop_label = str_translator(prop_details['labels']['en']['value'])
                label_list[prop] = prop_label
            except:
                non_labelled_props.append(prop)
                list_properties_copy.remove(prop)
    
    list_properties = list_properties_copy
    
    #For all values per property, label is extracted for each value ID [Q##### format]
    for prop in list_properties:
        
        labelled_values = []
       
        for value in list_prop_value[prop]:
            
            #Entities which directly have a value instead of an ID for an entity are saved
            if value['mainsnak']['snaktype'] == 'value' and isinstance(value['mainsnak']['datavalue']['value'], str):
                labelled_values.append(str_translator(value['mainsnak']['datavalue']['value']))
                
            #There are entities whose values are in form of Dictionary of values and not a string. These types
            #are checked here
            elif value['mainsnak']['snaktype'] == 'value' and isinstance(value['mainsnak']['datavalue']['value'], dict):
                
                #Extracting labels for Entities saved in terms of IDs
                if 'id' in value['mainsnak']['datavalue']['value'].keys():
                    
                    value_id = value['mainsnak']['datavalue']['value']['id']
                    value_label = ''
                    
                    #Extracted labels are stored in label_list for faster computation
                    if value_id not in label_list.keys():
                        
                        value_details = get_entity_dict_from_api(value_id)
                        
                        if 'hi' in value_details['labels'].keys():
                            value_label = value_details['labels']['hi']['value']
                            label_list[value_id] = value_label
                        
                        elif 'en' in value_details['labels'].keys():
                            value_label = str_translator(value_details['labels']['en']['value'])
                            label_list[value_id] = value_label

                    if value_label != '' or value_id in label_list.keys():
                        labelled_values.append(label_list[value_id])
                    
                else:
                    labelled_values.append(extract_dict_hindi_labels(value['mainsnak']['datavalue']['value']))
        
        if labelled_values:
            monument_labelled_prop_val[label_list[prop]] = labelled_values
    
    labelled_monument_list[monument['id']] = monument_labelled_prop_val
    
    count_monuments = count_monuments + 1
    
    if count_monuments%20 == 0:
        partition_num = str(count_monuments/20).split('.')[0]
        with open('../Data/Hindi_Labelled_Wikidata/hi_labelled_part'+ partition_num + '.json', 'w') as fout:
            json.dump(labelled_monument_list, fout)
        
        labelled_monument_list = {}
        
        print("Checkpoint %d reached, JSON dumps saved |" % (count_monuments/20), end = ' ')
        print("Time Elapsed:", end = ' ')
        print(time.time()-t0)
    
t1 = time.time()
total = t1-t0


# In[ ]:


print(total)
labelled_monument_list


# In[ ]:




