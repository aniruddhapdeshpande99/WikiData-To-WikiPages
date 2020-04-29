import json

wiki_template = {}

with open('../Data/Films/temp.json') as f:
    wiki_template = json.load(f)

wiki_nlg = ""

with open('../Data/Films/temp2.json') as f:
    wiki_nlg = json.load(f)

wikipage = wiki_template

wikipage['article'] = wikipage['article'] + wiki_nlg
