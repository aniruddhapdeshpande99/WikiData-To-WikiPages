import json

monument_list, hindi_monument_wikipedia = {}, []

# for i in range(1,103):
#     with open('../Data/English_Labelled_Wikidata/en_labelled_part'+str(i)+'.json') as f:
#         monument_list.update(json.load(f))

with open('../Data/Hindi_Labelled_Wikidata/hi_labelled_prop_values.json') as f:
    monument_list = json.load(f)

f = open('../Data/WikiBio_Styled_Formatted_Data/Hindi_Monuments/test/test.id', 'r')

g = open('../Data/WikiBio_Styled_Formatted_Data/Hindi_Monuments/train/train.id', 'r')

x = open('../Data/WikiBio_Styled_Formatted_Data/Hindi_Monuments/valid/valid.id', 'r')

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

train_box = open('../Data/WikiBio_Styled_Formatted_Data/Hindi_Monuments/train/train.box', 'w+')
test_box = open('../Data/WikiBio_Styled_Formatted_Data/Hindi_Monuments/test/test.box', 'w+')
valid_box = open('../Data/WikiBio_Styled_Formatted_Data/Hindi_Monuments/valid/valid.box', 'w+')

for monument in train:
	for val in monument.values():
		for key, val in val.items():
			x = "_".join(key.split())
			if isinstance(val[0], dict):
				for key1, val1 in val[0].items():
					if len(str(val1).split()) == 1:
						y = x + "_" + key1 + "_" + "1" + ":" + str(val1) + '\t'
						train_box.write(y)
					else:
						length = len(str(val1).split())
						for i in range(1, length + 1):
							z = x + "_" + key1 + "_" + "1" + "_" + str(i) + ":" + str(val1).split()[i - 1] + '\t'
							train_box.write(z)
			else:
				for value in val:
					if len(str(value).split()) == 1:
						k = x + "_" + "1" + ":" + str(value) + "\t"
						train_box.write(k)
					else:
						for i in range(1, len(str(value).split()) + 1):
							m = x + "_" + "1" + "_" + str(i) + ":" + str(value).split()[i - 1] + "\t"
							train_box.write(m)
	train_box.write("\n")

for monument in test:
	for val in monument.values():
		for key, val in val.items():
			x = "_".join(key.split())
			if isinstance(val[0], dict):
				for key1, val1 in val[0].items():
					if len(str(val1).split()) == 1:
						y = x + "_" + key1 + "_" + "1" + ":" + str(val1) + '\t'
						test_box.write(y)
					else:
						length = len(str(val1).split())
						for i in range(1, length + 1):
							z = x + "_" + key1 + "_" + "1" + "_" + str(i) + ":" + str(val1).split()[i - 1] + '\t'
							test_box.write(z)
			else:
				for value in val:
					if len(str(value).split()) == 1:
						k = x + "_" + "1" + ":" + str(value) + "\t"
						test_box.write(k)
					else:
						for i in range(1, len(str(value).split()) + 1):
							m = x + "_" + "1" + "_" + str(i) + ":" + str(value).split()[i - 1] + "\t"
							test_box.write(m)
	test_box.write("\n")

for monument in valid:
	for val in monument.values():
		for key, val in val.items():
			x = "_".join(key.split())
			if isinstance(val[0], dict):
				for key1, val1 in val[0].items():
					if len(str(val1).split()) == 1:
						y = x + "_" + key1 + "_" + "1" + ":" + str(val1) + '\t'
						valid_box.write(y)
					else:
						length = len(str(val1).split())
						for i in range(1, length + 1):
							z = x + "_" + key1 + "_" + "1" + "_" + str(i) + ":" + str(val1).split()[i - 1] + '\t'
							valid_box.write(z)
			else:
				for value in val:
					if len(str(value).split()) == 1:
						k = x + "_" + "1" + ":" + str(value) + "\t"
						valid_box.write(k)
					else:
						for i in range(1, len(str(value).split()) + 1):
							m = x + "_" + "1" + "_" + str(i) + ":" + str(value).split()[i - 1] + "\t"
							valid_box.write(m)
	valid_box.write("\n")
