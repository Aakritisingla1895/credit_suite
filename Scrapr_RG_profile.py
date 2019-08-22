import json
import os
import requests
from bs4 import BeautifulSoup as BS
from test import search
from pprint import pprint

#import MySQLdb
import os
#from getJSExecutedHTML import getJSExecutedHTML

import csv
with open('E:/Profeza/task_profeza/writeData.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

author_url_1 = 'https://www.researchgate.net/profile/Gilles_Malherbe'
author_url_2 = 'https://www.researchgate.net/profile/David_Humphreys10'
author_url_3 = 'https://www.researchgate.net/profile/Emma_Dave'

article_url = 'https://www.researchgate.net/publication/332449458_A_robust_fractionation_method_for_protein_subcellular_localization_studies_in_Escherichia_coli'

def get_proxy():
    proxy=requests.get('http://34.213.20.241/?Key=PROFEZA').text.split('\\')[1][1:]
    return proxy

try:
    from test import search

except ImportError:
    print("No module named 'google' found")
    # to search
for j in search(author_url_1, tld="co.in", num=10, stop=1, pause=2):
    result = j
    print(j)

def scrape_author_details(author_url_1):
    i=1
    while i>0:
        if i<=100:
            try:
                proxies = {'https': 'https://'+ get_proxy()}
                repo = requests.get(result, proxies=proxies,timeout=10)
                print('Our work is done.')
                break
            except:
                i+=1
                print("pass")
                continue
            else:
                print("under 50 count, website is blocking our proxy.")
                break
    soup = BS(repo.text, 'lxml')
    id = soup.findAll("meta", property="rg:id")
    for i in range(len(id)):
        author_id = id[i]['content']
        print ("Author id = ", author_id)

    name = soup.findAll("meta", property="twitter:title")
    for i in range(len(name)):
        author_name = name[i]['content']
        print ("Author name is : ", author_name)

    title = soup.findAll("meta", property="og:title")
    for i in range(len(title)):
        author_affiliation = title[i]['content']
        print (author_affiliation)
        try:
            if each_div.find_all('div', {'class': 'nova-e-text'})[1].text == "Research items":
                print ('found')
                research_items = int(each_div.find_all('div', {'class': 'nova-e-text'})[0].text.replace(',', ''))

        except Exception :
            for each_div in soup.find_all('div', {'class': 'nova-o-grid__column nova-o-grid__column--width-4/12@s-up'}):
                # getting citation details, reads and research item
                if each_div.find_all('div')[1].text == "Research items":
                    research_items = int(each_div.find_all('div')[0].text.replace(',', ''))
                    print ("Research items are : ", research_items)

                    skills = soup.find_all('a', {'class': 'nova-e-badge--radius-full'})
                    skills = [skill.text for skill in skills]
                    for x in range(len(skills)):
                        print ("Skills are", skills[x])
            try:
                if each_div.find_all('div', {'class': 'nova-e-text'})[1].text == "Citations":
                    print ('found')
                    citations = int(each_div.find_all('div', {'class': 'nova-e-text--size-xl'}))

            except Exception :
                for each_div in soup.find_all('div', {'class': 'nova-o-grid__column nova-o-grid__column--width-4/12@s-up'}):
            # getting citation details, reads and research item
                    if each_div.find_all('div')[1].text == "Citations":
                        citations = int(each_div.find_all('div')[0].text.replace(',', ''))
                        print ("citations are : ", citations)

                    try:
                        if each_div.find_all('div', {'class': 'nova-e-text'})[1].text == "Reads":
                            print ('found')
                            reads = int(each_div.find_all('div', {'class': 'nova-e-text--size-xl'}))

                    except Exception:
                        for each_div in soup.find_all('div', {'class': 'nova-o-grid__column nova-o-grid__column--width-4/12@s-up'}):
                            if each_div.find_all('div')[1].text == "Reads":
                                reads = int(each_div.find_all('div')[0].text.replace(',', ''))
                    print ("Reads are : ", reads)

    
    
        
print (scrape_author_details(author_url_1))



