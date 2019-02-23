#!/usr/bin/python3
# -*- coding: utf8 -*-

from pytube import Playlist

if __name__ == '__main__' :

    output_path = '_Output'
    url_playlist = 'https://www.youtube.com/playlist?list=PLW3Zl3wyJwWOpdhYedlD-yCB7WQoHf-My'

    pl = Playlist(url_playlist)

    pl.populate_video_urls()
    for link in pl.video_urls :
        print(str(link))

    #pl.download_all(download_path = output_path)

