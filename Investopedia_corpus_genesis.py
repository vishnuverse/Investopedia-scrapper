import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

def get_term_links_from_page(url):

    response = requests.get(url, allow_redirects=True)

    soup = BeautifulSoup(response.content, 'lxml')
    soup.find_all("ol", class_="list gaEvent")
    links = [a['href'] for div in soup.find_all("ol", attrs={"class": "list gaEvent"}) for a in div.find_all('a')]


    return links

#url='https://www.investopedia.com/terms/a/abandonment-and-salvage.asp'
def get_content_from_termpage(url):

    response = requests.get(url, allow_redirects=True)

    page_soup = BeautifulSoup(response.content, 'lxml')

    term = \
        page_soup\
        .find_all("div", {"class": "layout-title only-fontsize-title article-author-bar"})[0]\
        .find_all("h1")[0].get_text()

    content_box = str(page_soup.find_all("div", {"class": "content-box content-box-term"})[0])

    paras = BeautifulSoup(content_box, 'lxml')
    definition = str(paras.find_all("p")[0].get_text())
    break_down = str(paras.find_all("p")[1].get_text())

    term_object = dict()
    term_object['term'] = term
    term_object['definition'] = definition
    term_object['break_down'] = break_down

    return term_object

feeds = {}
#term_links=get_term_links_from_page('https://www.investopedia.com/categories/insurance.asp?page=4')
for i in range(0,11):
    term_links=get_term_links_from_page('https://www.investopedia.com/categories/insurance.asp?page='+str(i))
    print(i)
    for x in term_links:
        print(x)
        try:
            term_page_content=get_content_from_termpage('https://www.investopedia.com'+x)
            feeds[term_page_content['term']] = term_page_content
        except IndexError:
            pass
        with open('Investopedia_Corpus_oct5.txt', 'w') as outfile:
            json.dump(feeds, outfile)

import json
import pandas as pd
            
with open('Investopedia_terms.txt', encoding='utf-8') as fh:
    data = json.load(fh)
    
df=pd.DataFrame(data)
df2=df.T
terms=df2[['term','definition','break_down']]
terms=terms.reset_index()
terms=terms.drop('index',1)
terms.to_csv('investopedia_corpus_final.csv')          
tweets = []
for line in open('questiontag.txt', 'r'):
    tweets.append(json.loads(line))
    

df=pd.read_csv('investopedia_corpus_final.csv')


data = []

intents = {}
for a,b in df.iterrows():
    term_object = {}
    patterns = []
    response = []
    print(b['term'])
    tag = 'what_'+str.strip(b['term']).replace(" ", "")
    for each in tweets:
        qn = each +" "+str(b['term'])
        patterns.append(qn)
    response.append(b['definition'])
    term_object['tag'] = tag
    term_object['patterns'] = patterns
    term_object['responses'] = response
    data.append(term_object)
intents = {"intents" : data}
#for j,x in df.iterrows():
#    print(x['term'])
#    term_object = {}
#    term_object['tag'] = 'what_'+str.strip(x['term']).replace(" ", "")
#    
#    for i in tweets:
#        print (i)
#        term_object['patterns'] = str(i+x['term'])
#        #data.append(term_object)
#    term_object['responses'] = x['definition']


with open('Investopedia_Corpus.json', 'w') as outfile:
    json.dump(intents, outfile)
