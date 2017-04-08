#!/usr/bin/python3
# -*- coding: utf8 -*-

from collections import defaultdict
from collections import OrderedDict

from random import randint

if __name__ == '__main__' :

    # OrderedDict
    a = OrderedDict()
    a['foo'] = 1
    a['bar'] = 2

    b = OrderedDict()
    b['foo'] = 'red'
    b['bar'] = 'blue'

    print('#OrderedDict')
    for (value1, value2) in zip(a.values(), b.values()) :
        print(value1, value2)
    print()

    # d
    print('#defaultdict')
    stats = defaultdict(int)
    stats['my_conter'] += 1
    print('stats["my_conter"]', stats['my_conter'])
    stats['my_conter'] += 1
    print('stats["my_conter"]', stats['my_conter'])
    print('stats["my_empty"]', stats['my_empty'])
    print()

    #------------------------------------------------------------------
    #normal dict problem

    a = {}
    a['foo'] = 1
    a['bar'] = 2
    
    while True :
        z = randint(99, 1014)
        b = {}
        for i in range(z) :
            b[i] = i

        b['foo'] = 1
        b['bar'] = 1

        for i in range(z) :
            del b[i]

        if str(b) != str(a) :
            break

    print('#normal dict')
    print(str(b))
    print(str(a))
