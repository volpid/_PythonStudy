#!/usr/bin/python3
# -*- coding: utf8 -*-

import os
import shutil
import urllib
import zipfile

from thread_pipeline import ClosableQueue, StoppableWorker
from urllib import request

def DownloadFile(item) :
    url = item['url']
    filename = item['filename']
    print('download :', url)

    with urllib.request.urlopen(url) as response :
        with open(filename, "wb") as outfile :
            print(filename)
            shutil.copyfileobj(response, outfile)
            return filename

def DecompressZip(filename) :
    if filename :
        print('extract : ', filename)
        absdir = os.path.dirname(os.path.abspath(filename))
        zfile = zipfile.ZipFile(filename, 'r')
        zfile.extractall(absdir)
        return filename

if __name__ == '__main__' :
    
    download_queue = ClosableQueue()
    unzip_queue = ClosableQueue()
    done_queue = ClosableQueue()
    
    queues = [download_queue, unzip_queue]

    intermediate = './_Intermediate/'
    if not os.path.exists(intermediate) :
        os.makedirs(intermediate)
        print('mkdir ', intermediate)

    urls = [        
        r'https://downloads.sourceforge.net/project/glew/glew/2.0.0/glew-2.0.0.zip?r=http%3A%2F%2Fglew.sourceforge.net%2F&ts=1492244263&use_mirror=jaist',
        r'https://downloads.sourceforge.net/project/glew/glew/2.0.0/glew-2.0.0-win32.zip?r=http%3A%2F%2Fglew.sourceforge.net%2F&ts=1492261002&use_mirror=jaist'        
    ]

    filenames = [
        r'glew-2.0.0.zip',
        r'glew-2.0.0-win32.zip'
    ]
    
    threads = [
        StoppableWorker(DownloadFile, download_queue, unzip_queue),
        StoppableWorker(DecompressZip, unzip_queue, done_queue),
    ]

    for thread in threads : 
        thread.start()

    for (url, filename) in zip(urls, filenames) :
        downloaditem = {'url' : url, 'filename' : intermediate + filename}
        download_queue.put(downloaditem)

    for queue in queues :        
        queue.close()
        queue.join()

    print('done ', done_queue.qsize())
