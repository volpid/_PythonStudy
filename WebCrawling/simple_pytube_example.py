#!/usr/bin/python3
# -*- coding: utf8 -*-

from pytube import YouTube

if __name__ == '__main__' :
    
    output_path = '_Output'
    url = 'https://www.youtube.com/watch?v=sKCF8A3XGxQ&index=2&list=PLW3Zl3wyJwWOpdhYedlD-yCB7WQoHf-My&t=5s'
    
    yt = YouTube(url)
    print(yt.title)
    print(yt.description)

    for stream in yt.streams.all() :
        print(str(stream))

    print('mp4s')
    for stream in yt.streams.filter(file_extension = 'mp4').all() :
        print(str(stream))
    
    #yt.streams.first().download(output_path = output_path)
    yt.streams.filter(file_extension = 'mp4', progressive = True).order_by('resolution').desc().first().download()