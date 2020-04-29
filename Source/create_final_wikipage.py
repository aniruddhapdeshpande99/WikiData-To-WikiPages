#This Code parses through the given JSON file and makes an HTML page to display that news article.

#Importing Libraries
import json
import os

#Preprocesses the text as per HTML and adds Article's title
def add_title(title):
    title = title.replace("\"","&quot;")
    title = title.replace("“", "&ldquo;")
    title = title.replace("”", "&rdquo;")
    return "<h1>" + title + "</h1>"

def add_link(title):
    words = title.split()

    html = "<a href=""https://hi.wikipedia.org/w/index.php?title="+words[0]
    if len(words) > 1:
        for word in words[1:]:
            html = html + "_" + word
    html = html + "> Original Wikipage </a>"
    return html

#Preprocesses the text as per HTML and adds Article's main text
def add_text(text):
    return "<p>" + text + "</p>"

def add_cast(cast):
    if not cast:
        return ""
    else:
        html = "<div id = 'leftbox'> <h3> पात्र </h3> <ul>"
        for member in cast:
            html+= "<li>" + member + "</li>"
        html += "</ul> </div>"
        return html

def add_awards(awards_won):
    if not awards_won:
        return ""
    else:
        html = "<div id = 'middlebox'> <h3> जीते हुए पुरस्कार </h3> <ul>"
        for member in awards_won:
            html+= "<li>" + member + "</li>"
        html += "</ul> </div>"
        return html

def add_nominations(nominations):
    if not nominations:
        return ""
    else:
        html = "<div id = 'rightbox'> <h3> पुरस्कार नामांकन </h3> <ul>"
        for member in nominations:
            html+= "<li>" + member + "</li>"
        html += "</ul> </div>"
        return html

def add_infobox(infobox):
    infobox_order = ['शैली','निदेशक', 'निर्माता', 'कास्ट मेंबर', 'द्वारा वितरित', 'उत्पादन कंपनी', 'प्रकाशन तिथि','पहलू अनुपात','लागत', 'बॉक्स ऑफिस', 'फिल्म या टीवी शो की मूल भाषा', 'मूल देश', 'आधिकारिक वेबसाइट']
    if not infobox:
        return ""
    else:
        html = "<div id='infobox'> <h2 id='infobox_title'> इन्फोबॉक्स </h2>"
        for tag in infobox_order:
            if tag in infobox.keys():
                html = html + "<div class = infobox_prop><b>" + tag + "</b> </div> <div class = infobox_value>"
                for value in infobox[tag]:
                    html = html + "<p>"+value+"</p>"
                html = html + "</div>"

        html = html + "</div> </div>"
        return html

#Calls every function above to compile the final html page and saves it
def make_html():
    wiki_template = {}

    with open('../Data/Films/temp.json') as f:
        wiki_template = json.load(f)

    wiki_nlg = ""

    with open('../Data/Films/temp2.json') as f:
        wiki_nlg = json.load(f)

    wikipage = wiki_template

    wikipage['article'] = wikipage['article'] + wiki_nlg

    output_file = open("../index.html", "w")
    style = "#infobox_title { text-align: center;} #infobox {border: 2px solid black; width: 20%; float:right; margin-right: 10%;} .infobox_prop { font-weight: bold; text-align: center; text-decoration: underline;} .infobox_value { text-align: center } #main_text { text-align: justify; width: 60%;  padding: 10px; float: left;} #leftbox { float:left; width:20%; height:280px;} #middlebox{ float:left; width:40%; } #rightbox{float:left; width:40%;}"
    html_text = "<!DOCTYPE html><html><head><style>"+style+"</style></head><body>"
    html_text = html_text + add_title(wikipage['film_details']['title']) + add_link(wikipage['film_details']['title']) + "<div> <div id = main_text>" + add_text(wikipage['article']) + add_cast(wikipage['cast']) + add_awards(wikipage['awards won']) + add_nominations(wikipage['nominated']) + "</div>"+ add_infobox(wikipage['infobox']) + "</body></html>"
    output_file.write(html_text)
    output_file.close()

    return
#Main function to call make_html()
def main():
  make_html()


#Calls Main function
if __name__== "__main__":
  main()
