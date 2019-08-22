import json
import random
import requests
import csv
import pickle
import pandas as pd 
from test import search
import numpy 

base_url = 'https://107h2kbvai.execute-api.ap-south-1.amazonaws.com/abc/preview?'

crossref_api_base_url='http://api.crossref.org/works/'


def get_url(base_url):
    f=open('rrd_documents_list.txt','rb')
    f1=str(f.read())

    a=(f1.split(","))
    list1=[]
    list1.append(a[0][3:-1])
    for x in range(1,len(a)-1):
        #print(a[x][5:-1])
        list1.append(a[x][5:-1])
    list1.append(a[len(a)-1][5:-6])
    #print(list1)

    completeLink=[]
    for i in list1:
        completeLink.append(base_url+i)
    return completeLink


def get_article_doi(url):
    try:
        req = requests.get(url)
        return req.json()['article_doi']
    except Exception as e:
        print('error loading data' + e)
        
    all_url= (get_url(base_url))

    article_doi = []
    o=0
    file=open('article_doi.csv','w')
    for url in all_url[0:]:
        crossref_url = crossref_api_base_url+get_article_doi(url)
        print(o,crossref_url)
        article_doi.append(crossref_api_base_url+get_article_doi(url))
    
        #pickle.dump(crossref_api_base_url+get_article_doi(url),file)
        reader = csv.reader(file, skipinitialspace=False,delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            article_doi.append(row)
            o+=1
        print (article_doi)
        file.close()

def get_article_title():
    data = pd.read_csv("article_doi.csv") 
    titles=[]
    for val in data.iloc[:,0]:
        req = requests.get(val)
        titles.append(req.json()['message']['title'][0])
    return titles

    print(titles)

#all_titles=(get_article_title())

#df=pd.DataFrame(all_titles)
#df.to_csv("article_title.csv", index=False)

