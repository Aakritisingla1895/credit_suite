import requests
import json
import re


import pandas as pd
from test import search
import time
from urllib.request import urlopen
from html.parser import HTMLParser
import random
from bs4 import BeautifulSoup as BS

url = "https://www.researchgate.net/publication/332449458_A_robust_fractionation_method_for_protein_subcellular_localization_studies_in_Escherichia_coli"

def get_proxy():
    proxy=requests.get('http://34.213.20.241/?Key=PROFEZA').text.split('\\')[1][1:]
    return proxy


def google_search_article_links():
    o = 0;
    links = []
    article_data = pd.read_csv("article_title.csv")
    google_search_links=[]
    for value in article_data.iloc[:,-1]:
        search_article = value  + "+researchgate"
        google_search_links = []
        google_search_links.append(search_article)

        #print (google_search_links)
        for j in search(search_article, tld="co.in", num=10, stop=1, pause=2):
            result = j
            o+=1
            #print (o, result)
            links.append(result)
            #print (o, links)
    #print ("Final result", links)
    return links
    result_links = google_search_article_links()
    #print (result_links)

#all_google_article_links = (google_search_article_links())
#print (all_google_article_links)

def get_article_title():

    article_data = pd.read_csv("google_search_articles.csv")


    for value in article_data.iloc[:,-1]:
        i=1
        while i>0:
            if i<=100:
                try:
                    proxies = {'https': 'https://'+ get_proxy()}
                    response = requests.get(value, proxies=proxies,timeout=10)

                    print('Our work is done.')
                    break
                except:
                    i+=1

                    print("pass")
                continue
            else:
                print("under 50 count, website is blocking our proxy.")
                break
            if len(response) <= 0:
                    continue
            try:
                soup = BS(response, 'lxml')
                article_title = soup.find_all('h1', {'class' : "publication-details__title"})[0].text.strip()
                break
            except Exception:
                continue
            break
        soup = BS(response.text, 'lxml').encode("utf-8")
        article_title = soup.find('h1', {'class' : "publication-details__title"})[0].text.strip()
        print (article_title)

        citations_div = soup.find_all('div', {'class': 'js-target-citation'})
        if len(citations_div) > 0:
            citations_div = citations_div[0]

        all_citations = citations_div.find_all('li', {'class': 'publication-citations__item'})
        for citation in all_citations:
            try:
                if citation.find_all('span', {'class': 'nova-v-publication-item__type'})[0].text == 'Article':
                    cited_publication_url = "https://www.researchgate.net/" + citation.find_all('div', {'itemprop': 'headline'})[0].find_all('a')[0]['href']
                    #get_publication_data(cited_publication_url, True, base_article_doi)
                    print (cited_publication_url)
            except Exception:
                # the span element not found
                continue
    else:
        print("No citations found")

       # print(soup.encode("utf-8"))


def get_first_degree_connections(article_url, base_doi=None):
    # take all authors and create thier profile if doesn't exists
    # dump this article data to db
    # link all the authors with this article doi
    # link all citations doi with this doi

    # dump all cited by articles doi
    # dump all cited by authors data
    article_data = pd.read_csv("google_search_articles.csv")


    for value in article_data.iloc[:,-1]:
        count = 0
        while True:
            try:
                proxy_add = get_proxy()
                req = requests.get(value, proxies={'https': 'https://'+proxy_add}, timeout=10).text
                # this request is to be made with selinium and all the author details should be returned
                # @Selinium Request
                #req = getJSExecutedHTML(article_url, proxy_add)
                #os.system('killall firefox')
                if len(req) <= 0:
                    continue
                try:
                    soup = BS(req, 'lxml')
                    article_title = soup.find_all('h1', {'class' : "publication-details__title"})[0].text.strip()
                    break
                except Exception:
                    continue
                break
            except Exception as e:
                count += 1
                print(e)
                print("Failed Count", count)
                continue
        print("422")
        soup = BS(req, 'lxml')
        article_title = soup.find_all('h1', {'class' : "publication-details__title"})[0].text.strip()
        total_citations = None
        for publication_summary in soup.find_all('div', {'class' : "publication-resources-summary__see-all-count"}):
            if publication_summary.text.split()[-1] == "Citations":
                total_citations = int(publication_summary.text.split()[0].replace(',', ''))
        # getting meta data of the article
        meta_div = soup.find_all('div', {'class' : "publication-meta"})[0]
        # print(meta_div)
        try:
                doi = meta_div.find_all('div', {'class': 'nova-e-text--color-grey-500'})[0].text.strip().split()[1]
        except Exception as e:
            print("Doi Not found", e)
            return
        total_reads = int(meta_div.find_all('div')[0].text.split('\u2002')[-1].split()[0].strip().replace(',', ''))
        try:
            publisher = meta_div.find_all('a')[0].text.strip()
        except Exception:
            publisher = None
        meta_data = meta_div.find_all('div')[0].text.split('\u2002')
        if len(meta_data) == 3:
            published_date = meta_data[0].split('\xa0')[-1].strip()
        else:
            published_date = meta_data[2].split('\xa0')[-1].strip()
        print(doi, article_title, publisher, published_date, total_citations, total_reads)
    #if dbutils.article_present_in_db(doi):
        return True
        print("448")
    # dump this article data to db
    #dbutils.store_article_data(doi, article_title, publisher, published_date, total_citations, total_reads, article_url)

    # get all authors
    profile_divs = soup.find_all('div', {'class': 'nova-v-person-list-item__align-content'})
    print("Profile Div len", len(profile_divs))
    is_first_author = False
    first_author_found = False
    for profile_div in profile_divs:
            if len(profile_div) > 0:
                if not is_first_author and not first_author_found:
                    # will only work for first author
                    is_first_author= True
                    first_author_found = True
                author_profile_url = profile_div.find_all('div', {'itemprop': 'name'})[0].find('a')['href']
                print (author_profile_url)
                #author_id = get_author_id(author_profile_url)

                is_first_author = False

    return True



def scrape_author_second_degree_connections():
    # populate base_article data if missing
    #author_articles = dbutils.get_author_articles(author_id)
    article_data = pd.read_csv("google_search_articles.csv")
    for each_article in article_data:
        base_article_url = each_article[2]
        count = 0
        while True:
            try:
                proxy_add = get_proxy()
                # this request is to be made with selinium and all the author details should be returned
                req = requests.get(base_article_url, proxies={'https': 'https://'+proxy_add}, timeout=10).text
                # req = getJSExecutedHTML(base_article_url, proxy_add)
                # os.system('killall firefox')
                if len(req) <= 0:
                    continue
                try:
                    soup = BS(req, 'lxml')
                    article_title = soup.find_all('h1', {'class' : "publication-details__title"})[0].text.strip()
                    break
                except Exception:
                    continue
                break
            except Exception as e:
                count += 1
                print(e)
                print(count)
                continue
        print("422")
        soup = BS(req, 'lxml')
        citations_div = soup.find_all('div', {'class': 'js-target-citation'})
        if len(citations_div) > 0:
            citations_div = citations_div[0]

            all_citations = citations_div.find_all('li', {'class': 'publication-citations__item'})
            for citation in all_citations:
                try:
                    if citation.find_all('span', {'class': 'nova-v-publication-item__type'})[0].text == 'Article':
                        cited_publication_url = "https://www.researchgate.net/" + citation.find_all('div', {'itemprop': 'headline'})[0].find_all('a')[0]['href']
                        #get_publication_data(cited_publication_url, True, base_article_doi)
                        print (cited_publication_url)
                except Exception:
                    # the span element not found
                    continue
        else:
            print("No citations found")


###################### TASK CREATE AUTHOR PUBLICATIONS######################






print (get_article_title())
