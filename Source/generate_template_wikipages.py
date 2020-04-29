#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing required libraries
import json
import re
import numpy as np
import random


# In[2]:


# Reads all the data necessary to generate the wikipage
def retrieve_data():

    en_prop_key = {
        'budget':'लागत',
        'narr locations' : 'कथा स्थल',
        'production company' : 'उत्पादन कंपनी',
        'artist' : 'कार्यकारी निर्माता',
        'ICAA rating' : 'आईसीएए रेटिंग',
        'series' : 'श्रृंखला का हिस्सा',
        'NMHH rating' : 'एनएमएचएच फिल्म रेटिंग' ,
        'nominated' : 'के लिए मनोनीत',
        'sequel' : 'बाद' ,
        'MPAA rating' : 'एमपीएए फिल्म रेटिंग',
        'release year' : 'प्रकाशन तिथि',
        'awards won' : 'पुरस्कार प्राप्त',
        'cast' : 'कास्ट मेंबर',
        'producer' : 'निर्माता' ,
        'website' : 'आधिकारिक वेबसाइट' ,
        'distributor' : 'द्वारा वितरित' ,
        'based on' : 'आधार पर',
        'director' : 'निदेशक',
        'country' : 'मूल देश',
        'editor' : 'फिल्म संपादक',
        'production designer' : 'प्रोडक्शन डिजाइनर',
        'singers' : 'संगीतकार',
        'topic' : 'मुख्य विषय',
        'fil locations' : 'फिल्मांकन स्थान',
        'music director' : 'कलाकार',
        'dir photo' : 'फोटोग्राफी के निदेशक',
        'FSK rating' : 'एफएसके फिल्म रेटिंग',
        'duration' : 'पहलू अनुपात',
        'colour': 'रंग',
        'box office' : 'बॉक्स ऑफिस',
        'costume designer' : 'कॉस्ट्यूम डिजाइनर',
        'lang' : 'फिल्म या टीवी शो की मूल भाषा',
        'screenwriter' : 'पटकथा लेखक' ,
        'genre' : 'शैली'
    }



    sentence_templates = []
    with open('../Data/Films/Films_Generated_Wikipages/template_sents.json') as f:
        sentence_templates = json.load(f)

    hi_labelled_films = {}
    with open('../Data/Films/Films_Hindi_Wikidata_Hi_Labelled/films_hi_labelled.json') as f:
        hi_labelled_films = json.load(f)

    film_ids = []
    with open('../Data/Films/WikiBio_Styled_Formatted_Data/train/train.id') as f:
        film_ids = f.readlines()
    film_ids = [x.strip() for x in film_ids]

    film_titles = []
    with open('../Data/Films/WikiBio_Styled_Formatted_Data/train/train.title') as f:
        film_titles = f.readlines()
    film_titles = [x.strip() for x in film_titles]

    film_urls = []
    for title in film_titles:
        film_urls.append("https://hi.wikipedia.org/w/index.php?title="+title)

    film_details = {}

    for i in range(0,len(film_ids)):
        film_details[film_ids[i]] = {'url':film_urls[i], 'title': film_titles[i], 'index':i}

    return film_details,sentence_templates, hi_labelled_films, en_prop_key


# In[3]:


#Retrieves all templates for the first line of the article
def get_first_sentences_templates(sentence_templates):
    first_sentences = []
    for sentence in sentence_templates:
        if '{{film}}' in sentence.split():
            first_sentences.append(sentence)

    return first_sentences


# In[4]:


#Retrieves a dictionary of list of tags present in a given sentence template for all the sentence_templates that
#are passed to it as an argument.
def retrieve_template_tags(sentence_templates):
    template_tags = {}
    for sentence_template in sentence_templates:
        template_tags[sentence_template] = re.findall(r'\{\{(.*?)\}\}', sentence_template)

    return template_tags


# In[5]:


#Retrieves a list of tags present within a single template sentence
def retrieve_sent_tags(sentence):
    return re.findall(r'\{\{(.*?)\}\}', sentence)


# In[6]:


#Returns the most complexly formatted first sentence template as possible for a given article
def retrieve_first_sentence_template(template_tags, article_props, en_prop_key):
    sentence_templates = list(template_tags.keys())
    first_sentences = get_first_sentences_templates(sentence_templates)
    first_sentences_tags = retrieve_template_tags(first_sentences)

    for sent in first_sentences_tags.keys():
        tags = first_sentences_tags[sent]
        tags.remove('film')
        first_sentences_tags[sent] = tags

    matching_template = ""
    max_template_size = 0

    for first_sent in first_sentences_tags.keys():
        tags  = first_sentences_tags[first_sent]
        hi_tags = [en_prop_key[tag] for tag in tags]

        if set(hi_tags) <= set(article_props) and len(hi_tags) > max_template_size:
            max_template_size = len(hi_tags)
            matching_template = first_sent

    return matching_template



# In[7]:


#Returns the most complexly formatted remaining sentence templates as possible for a given article
#as the remaining properties for that article keep reducing.
def retrieve_remaining_sentence_template(remaining_template_tags, remaining_article_props, en_prop_key):
    matching_template = ""
    max_template_size = 0

    for remaining_sent in remaining_template_tags.keys():
        tags  = remaining_template_tags[remaining_sent]
        hi_tags = [en_prop_key[tag] for tag in tags]

        if set(hi_tags) <= set(remaining_article_props) and len(hi_tags) > max_template_size:
            max_template_size = len(hi_tags)
            matching_template = remaining_sent

    return matching_template


# In[8]:


#Based on the current stage of the article template, this function returns what properties about that article are
#remaining to be put inside the article template
def update_remaining_props(template_tags, article_props, article, en_prop_key):
    article_tags = retrieve_sent_tags(article)
    new_template_tags = {}

    for template_sent in template_tags.keys():
        flag = 1
        tags = template_tags[template_sent]
        for tag in article_tags:
            if tag in tags:
                flag = 0
                break
        if flag == 1:
            new_template_tags[template_sent] = template_tags[template_sent]

    article_tags.remove('film')
    used_props = [en_prop_key[tag] for tag in article_tags]

    new_article_props = []
    for prop in article_props:
        if prop not in used_props:
            new_article_props.append(prop)

    return new_template_tags, new_article_props



# In[9]:


#Returns the Contents of the Categories - Cast, Awards, Nominations, Ratings for the movie
#It also returns the Infobox contents for a movie.
def get_categories_infobox(film):

    currencies = {'Q80524':'रुपये',
                  'Q41044':'रूबल',
                  'Q1137675':'करोड़ रुपये',
                  'Q4916':'यूरो',
                  'Q25224':'पौंड',
                  'Q14083':'डॉलर',
                  'Q31015':'होन्ग कोंग डॉलर',
                  'Q4917':'डॉलर',
                  '1':'डॉलर'}

    awards = []
    nominations = []

    if 'पुरस्कार प्राप्त' in film.keys():
        awards = film['पुरस्कार प्राप्त']

    if 'के लिए मनोनीत' in film.keys():
        nominations = film['के लिए मनोनीत']

    cast = []
    infobox = {}

    if 'कास्ट मेंबर' in film.keys():
        cast = film['कास्ट मेंबर']
        if len(cast) > 7:
            infobox['कास्ट मेंबर'] = cast[:7]
        else:
            infobox['कास्ट मेंबर'] = cast

    if 'लागत' in film.keys():
        link = film['लागत'][0]['इकाई']
        amount = film['लागत'][0]['राशि'].split('+')[-1]
        currency = currencies[link.rsplit('/', 1)[-1]]
        infobox['लागत'] = [amount + " " + currency]

    if 'बॉक्स ऑफिस' in film.keys():
        link = film['बॉक्स ऑफिस'][0]['इकाई']
        amount = film['बॉक्स ऑफिस'][0]['राशि'].split('+')[-1]
        currency = currencies[link.rsplit('/', 1)[-1]]
        infobox['बॉक्स ऑफिस'] = [amount + " " + currency]

    if 'प्रकाशन तिथि' in film.keys():
        date = film['प्रकाशन तिथि'][0]['समय']
        year = re.findall('\+[\s]*(.*?)\-', date)[0]
        month = re.findall('\-(.*?)\-', date)[0]
        day = re.findall('\-(.*?)T', date)[0][-2:]
        infobox['प्रकाशन तिथि'] = [day + "/" + month + "/" + year]

    if 'पहलू अनुपात' in film.keys():
        infobox['duration'] = film['पहलू अनुपात'][0]


    remaining_infobox_entities = ['उत्पादन कंपनी', 'श्रृंखला का हिस्सा', 'निर्माता','आधिकारिक वेबसाइट', 'द्वारा वितरित', 'निदेशक' ,'मूल देश', 'संगीतकार', 'फिल्म या टीवी शो की मूल भाषा','शैली']

    for entity in remaining_infobox_entities:
        if entity in film.keys():
            infobox[entity] = film[entity]

    return cast, awards, nominations, infobox




# In[10]:


#Fills in values inside the article template.
def fill_in_template(film_wiki_props, article, en_prop_key, film_data):
    title = film_data['title']
    url = film_data['url']
    currencies = {'Q80524':'रुपये',
                  'Q41044':'रूबल',
                  'Q1137675':'करोड़ रुपये',
                  'Q4916':'यूरो',
                  'Q25224':'पौंड',
                  'Q14083':'डॉलर',
                  'Q31015':'होन्ग कोंग डॉलर',
                  'Q4917':'डॉलर',
                  '1':'डॉलर'}

    content_dict = {}

    for prop in film_wiki_props:
        for en_prop in en_prop_key.keys():
            if prop == en_prop_key[en_prop]:
                content_dict[en_prop] = film_wiki_props[prop]
                break

    article_tags = retrieve_sent_tags(article)
    article_content_string = {}
    article_content_string['film'] = title
    article_tags.remove('film')

    for tag in article_tags:
        if tag == 'release year':
            article_content_string[tag] = re.findall('\+[\s]*(.*?)\-', content_dict[tag][0]['समय'])[0]
        elif tag == 'box office' or tag == 'budget':
            link = content_dict[tag][0]['इकाई']
            amount = content_dict[tag][0]['राशि'].split('+')[-1]
            currency = currencies[link.rsplit('/', 1)[-1]]
            article_content_string[tag] = amount + " " + currency

        elif tag == 'narr locations' or tag == 'fil locations' or tag == 'singers':
            content_arr = content_dict[tag]
            filling_text = ""
            if len(content_arr) == 1:
                filling_text = content_arr[0]
            else:
                filling_text = content_arr[0]
                for content in content_arr[1:]:
                    filling_text = filling_text + ", " + content

            article_content_string[tag] = filling_text

        elif tag == "screenwriter" or tag == "producer" or tag == 'director':
            content_arr = content_dict[tag]
            filling_text = ""
            if len(content_arr) == 1:
                filling_text = content_arr[0]
            else:
                filling_text = content_arr[0]
                count = 1
                for content in content_arr[1:]:
                    if count > 3:
                        break
                    else:
                        filling_text = filling_text + ", " + content
                        count+=1

            article_content_string[tag] = filling_text

        elif tag == 'cast' or tag == 'awards won' or tag == 'nominated':
            content_arr = content_dict[tag]
            filling_text = ""
            if len(content_arr) == 1:
                filling_text = content_arr[0]
            else:
                filling_text = content_arr[0]
                count = 1
                for content in content_arr[1:]:
                    if count > 5:
                        break
                    else:
                        filling_text = filling_text + ", " + content
                        count+=1

            article_content_string[tag] = filling_text

        else:
            article_content_string[tag] = content_dict[tag][0]

    for tag in article_content_string.keys():
        pattern = '\{\{'+tag+'\}\}'
        article = re.sub(pattern, article_content_string[tag], article)

    return article.strip()



# In[11]:


#Creates the entire wikipage based on using above functions.
#For article generation, it keeps updating the remaining properties as newer article template sentences are
#added. (This can be seen in the "while article_props:" line.)
def create_wikipage(film_id, film_details, sentence_templates, hi_labelled_films, en_prop_key):
    template_tags = retrieve_template_tags(sentence_templates)
    total_props = np.array(list(en_prop_key.values()))
    total_props = list(np.unique(total_props))

    film = hi_labelled_films[film_id]
    film_wiki_props = {}

    for prop in total_props:
        if prop in film.keys():
            film_wiki_props[prop] = film[prop]

    article_props = set(list(film_wiki_props.keys()))
    non_article_props = set(['पहलू अनुपात', 'आईसीएए रेटिंग', 'एफएसके फिल्म रेटिंग', 'आधिकारिक वेबसाइट', 'उत्पादन कंपनी', 'एमपीएए फिल्म रेटिंग', 'एनएमएचएच फिल्म रेटिंग'])
    article_props = article_props.difference(non_article_props)
    article_props = list(article_props)

    article = retrieve_first_sentence_template(template_tags, article_props , en_prop_key)
    if article == "":
        article = "{{film}} एक फिल्म है।"

    while article_props:
        template_tags, article_props = update_remaining_props(template_tags, article_props, article, en_prop_key)
        article = article + retrieve_remaining_sentence_template(template_tags, article_props, en_prop_key)

    article = fill_in_template(film_wiki_props, article, en_prop_key, film_details[film_id])

    cast, awards, nominations, infobox = get_categories_infobox(film_wiki_props)

    wikipage = {}
    wikipage['article'] = article
    wikipage['cast'] = cast
    wikipage['awards won'] = awards
    wikipage['nominated'] = nominations
    wikipage['infobox'] = infobox

    return wikipage


# In[12]:


def main():

    print("Loading Template Sentences Data")

    #Retrieving Needed Data and creating a Wikipage using template sentences.
    film_details,sentence_templates, hi_labelled_films, en_prop_key = retrieve_data()
    page_key = random.choice(list(hi_labelled_films.keys()))
    wikipage = create_wikipage(page_key, film_details, sentence_templates, hi_labelled_films, en_prop_key)
    wikipage['film_details'] = film_details[page_key]
    print(wikipage)
    with open("../Data/Films/temp.json", 'w') as f:
        json.dump(wikipage,f)

if __name__ == "__main__":
    main()
