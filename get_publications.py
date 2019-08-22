import re
import requests
import json
from pprint import pprint
import random
from bs4 import BeautifulSoup
from googlesearch import search
from lxml import html
import time
import uuid
import traceback
import sys

import MySQLdb
import os

def get_proxy():
    return json.loads(requests.get('http://34.213.20.241/?Key=PROFEZA').text)[1:-1]

def get_author_id(author_profile_url):
    if 'scientific-contributions' in author_profile_url:
        return author_profile_url[author_profile_url.find('scientific-contributions')+25:]
    elif 'profile' in author_profile_url:
        return author_profile_url[author_profile_url.find('profile')+8:]
print (get_author_id("https://www.researchgate.net/profile/David_Humphreys10"))

def get_page_type(page_url):
    if 'scientific-contributions' in page_url:
        return 1
    elif 'profile' in page_url:
        return 2
    elif 'publication' in page_url:
        return 3
print (get_page_type("https://www.researchgate.net/profile/David_Humphreys10"))

def get_publications(profile_url):
    print(profile_url)
    while True:
        try:
            proxy_add = get_proxy()
            print(proxy_add)
            req = requests.get(profile_url, proxies={'https': 'https://'+proxy_add}, timeout=10)
            soup = BeautifulSoup(req.text, 'lxml')
            if "We've picked up some unusual traffic from your network and have temporarily blocked access from your IP address." in soup.text:
                continue
            if "Please, wait while we are validating your browser" in soup.text:
                continue
            break
        except Exception as e:
            print(e)
            continue

    all_publications = soup.find_all('div', {'class' : 'nova-v-publication-item__body'})

    # if user had multiples articles:
    next_page_url = ""
    try:

        next_page_url = soup.find_all('div', {'class': 'nova-o-stack__item pagination'})[0].find_all('a')[2]['href']
        if profile_url == next_page_url:
            next_page_url = ""
    except Exception:
        print("Cant find next page profile_url")
        next_page_url = ""
        pass
    print(all_publications, next_page_url)
    return (all_publications, next_page_url)
print (get_publications("https://www.researchgate.net/scientific-contributions/2152823659_Gilles_Malherbe"))
