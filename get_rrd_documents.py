import requests
from pprint import pprint
from bs4 import BeautifulSoup
import lxml
import json
import random
from test import search
import pickle
import string

 x = 0
base_url = 'https://107h2kbvai.execute-api.ap-south-1.amazonaws.com/abc/preview?'

url = 'https://107h2kbvai.execute-api.ap-south-1.pyamazonaws.com/abc/preview?id=f86e58e8bdd74719b92d745b0fdedf24&sub_id=f787eb8c-74f4-45ea-8553-71e803241cdb&version=-1'

crossref_api_base_url='http://api.crossref.org/works'

response = requests.get(url)
pprint(response.text)

#fetching url with different id and sub_id
def get_id_sub_id(url):
    val1=url.split('?')[1]
    return val1


#fetching base article doi
def get_base_article_doi(base_url,val1):
    try:
        req_url = base_url+val1

        req = requests.get(req_url)
        return req.json()['article_doi']
    except Exception as e:
        print('error loading data' + e)
#fetch base_article_url

#function to get article title from base article url
def get_article_title(base_url,val):
    try:
        crossref_api__url=str(base_url+val)
        req = requests.get(crossref_api__url)
        article_title = req.json()['message']['title'][0]
        return article_title

        title_name = get_article_title()
    except :
        print('Not valid')

#getting google results
def get_google_results(title_name):
    try:
        from test import search
        search_article = str(title_name  + "+researchgate")
        for j in search(search_article, tld="co.in", num=10, stop=1, pause=2):
            result = j
    except ImportError:
        print("No module named 'google' found")
    # to search

    return result

val1=get_id_sub_id(url)
val2=get_base_article_doi(base_url,val1)
val3 =get_article_title(crossref_api_base_url,val2)

print ("doi=",val2,"\n","article_title=", val3)
print (get_google_results(val3) +str(val3))
