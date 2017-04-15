#!/usr/bin/python3
# -*- coding: utf8 -*-

from queue import Queue
from threading import Lock
from threading import Thread

def download(item) :
    print(item, ' download')
    return item

def resize(item) :
    print(item, ' resize')
    return item

def upload(item) :
    print(item, ' upload')
    return item

class ClosableQueue(Queue) :
    SENTINEL = object()

    def close(self) :
        self.put(self.SENTINEL)

    def __iter__(self) :
        while True :
            item = self.get()

            try :
                if item is self.SENTINEL :
                    return
                yield item
            finally :
                self.task_done()

class StoppableWorker(Thread) :
    def __init__(self, func, in_queue, out_queue) :
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        for item in self.in_queue :
            result = self.func(item)
            if result is not None :
                self.out_queue.put(result)

if __name__ == '__main__' :
    download_queue = ClosableQueue()
    resize_queue = ClosableQueue()
    uplaod_queue = ClosableQueue()
    done_queue = ClosableQueue()

    threads = [
        StoppableWorker(download, download_queue, resize_queue),
        StoppableWorker(resize, resize_queue, uplaod_queue),
        StoppableWorker(upload, uplaod_queue, done_queue),
    ]

    for thread in threads : 
        thread.start()

    for num in range(10) :
        download_queue.put(num)

    download_queue.close()
    download_queue.join()
    resize_queue.close()
    resize_queue.join()
    uplaod_queue.close()
    uplaod_queue.join()

    print(done_queue.qsize(), ' item finishied')