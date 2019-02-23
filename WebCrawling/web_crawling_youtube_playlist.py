#!/usr/bin/python3
# -*- coding: utf8 -*-

import json
import requests

from bs4 import BeautifulSoup

if __name__ == '__main__' :
    
    url_playlist = 'https://www.youtube.com/playlist?list=PLW3Zl3wyJwWOpdhYedlD-yCB7WQoHf-My'
    url_watch = 'https://www.youtube.com/watch?v='

    windowYTInitialDataTxt = 'window["ytInitialData"] = '

    header_request = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    }

    response = requests.get(url_playlist, headers = header_request)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')
    
    foundIdx = -1
    for (idx, script) in enumerate(scripts) :
        if windowYTInitialDataTxt in str(script) :
            foundIdx = idx
            print("#found")
            break;

    if foundIdx < 0 :
        print('Can\'t find playlist')

    rawText = scripts[foundIdx].get_text()
    stripText = rawText.strip().split(windowYTInitialDataTxt)[1].split(';\n')[0]
    
    jsonData = json.loads(stripText, encoding = 'utf8', strict = False)
    
    jsonSubDatat = jsonData['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']

    playlist = []        
    for sub in jsonSubDatat :
        if 'unplayableText' not in sub['playlistVideoRenderer'] :
            playlist.append(str(print(sub['playlistVideoRenderer']['videoId']))
    
    for link in playlist :
        print(url_watch + link)