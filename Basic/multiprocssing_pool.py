#!/usr/bin/python3
# -*- coding: utf8 -*-

from multiprocessing import Pool

import time

def mp_worker(input) :
    print('process %s waiting %s sec' %(input[0], input[1]))
    time.sleep(int(input[1]))
    print('process %s done' % input[0])

def mp_handler() :
    p = Pool(2)
    p.map(mp_worker, data)

if __name__ == '__main__' :
    data = (['a', '2'], ['b', '4'], ['c', '3'], ['d', '9'],
            ['e', '1'], ['f', '7'], ['g', '2'], ['h', '1'])

    mp_handler()
