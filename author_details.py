import json
import requests
from bs4 import BeautifulSoup
from get_rrd_documents import get_article_title, get_google_results

url = 'https://www.researchgate.net/publication/332449458_A_robust_fractionation_method_for_protein_subcellular_localization_studies_in_Escherichia_coli'
def get_proxy():
    proxy=requests.get('http://34.213.20.241/?Key=PROFEZA').text.split('\\')[1][1:]
    return proxy

def get_author_details(url):
    i=1
    while i>0:
        if i<=100:
            try:
                proxies = {'https': 'https://'+ get_proxy()}
                response = requests.get(url,proxies=proxies,timeout=10)
                print('Our work is done.')
                break
            except:
                i+=1
                print("pass")
                continue
            else:
                print("under 50 count, website is blocking our proxy.")
                break
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.findAll("meta", property="citation_author")
    list=[]
    for i in range(len(title)):
        #result = []
        author_details_rg = title[i]['content']
        list.append(author_details_rg)
    return list
        #return result

print (get_author_details(url))
