import json

monument_list, hindi_monument_wikipedia = [], []

with open('../../Downloads/WikiData-To-WikiPages/Data/Hindi_Labelled_Wikipages/labelled_prop_values.json') as f:
	monument_list = json.load(f)

f = open('../../Downloads/WikiData-To-WikiPages/Data/Formatted_Data/test/test.id', 'r')

g = open('../../Downloads/WikiData-To-WikiPages/Data/Formatted_Data/train/train.id', 'r')

x = open('../../Downloads/WikiData-To-WikiPages/Data/Formatted_Data/valid/valid.id', 'r')

train_ids = g.read().split('\n')[:-1]

test_ids = f.read().split('\n')[:-1]

valid_ids = x.read().split('\n')[:-1]

combined_ids = test_ids + train_ids + valid_ids

for i in range(len(combined_ids)):
	for key in monument_list.keys():
		if combined_ids[i] == key:
			hindi_monument_wikipedia.append({key:monument_list[key]})

train, test, valid = [], [], []

for i in range(len(train_ids)):
	for monument in hindi_monument_wikipedia:
		for key in monument.keys():
			if key == train_ids[i]:
				train.append(monument)
				break

for i in range(len(test_ids)):
	for monument in hindi_monument_wikipedia:
		for key in monument.keys():
			if key == test_ids[i]:
				test.append(monument)
				break

for i in range(len(valid_ids)):
	for monument in hindi_monument_wikipedia:
		for key in monument.keys():
			if key == valid_ids[i]:
				valid.append(monument)
				break

f = open('train.box', 'w+')

for monument in train:
	for val in monument.values():
		for key, val in val.items():
			x = "_".join(key.split())
			if isinstance(val[0], dict):
				for key1, val1 in val[0].items():
					if len(str(val1).split()) == 1:
						y = x + "_" + key1 + "_" + "1" + ":" + str(val1) + '\t'
						f.write(y)
					else:
						length = len(str(val1).split())
						for i in range(1, length + 1):
							z = x + "_" + key1 + "_" + "1" + "_" + str(i) + ":" + str(val1).split()[i - 1] + '\t'
							f.write(z)
			else:
				for value in val:
					if len(str(value).split()) == 1:
						k = x + "_" + "1" + ":" + str(value) + "\t"
						f.write(k)
					else:
						for i in range(1, len(str(value).split()) + 1):
							m = x + "_" + "1" + "_" + str(i) + ":" + str(value).split()[i - 1] + "\t"
							f.write(m)
	f.write("\n")