#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys

def multiply(a, b) :
    print('will compute', a, 'times', b)
    c = 0
    for i in range(0, a) :
        c = c + b
    return c

if __name__ == '__main__' :
    print(multiply(10, 20))
