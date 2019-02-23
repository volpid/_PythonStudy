#!/usr/bin/python3
# -*- coding: utf8 -*- 

import json
import requests

from requests import Session
from bs4 import BeautifulSoup

if __name__ == '__main__' :

    url = 'http://httpbin.org/post'
    
    request_header = {
        'X-Requested-With': 'XMLHttpRequest',
        #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        #'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': url
    }

    get_param = {
        "param1" : 'A',
        "param2" : 1
    }

    get_param_json = json.dumps(get_param);

    cookie = {
        'id' : 'cookie1234'
    }
    
    response = requests.post(url = url, headers = request_header, data = get_param, cookies = cookie)    
    #print(response.text)
    print(response.json())

    response = requests.post(url = url, headers = request_header, data = get_param_json, cookies = cookie)
    #print(response.text)
    print(response.json())

    session = Session()
    session.head(url)
    response = session.post(url = url, headers = request_header, data = get_param, cookies = cookie)    
    #print(response.text)
    print(response.json())

    url_google = 'http://www.google.co.kr'
    response = requests.get(url_google)
    #print(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')
    hiperlinks = soup.find_all('a')
    for link in hiperlinks :
        print(link.text + " : " + link['href'])
