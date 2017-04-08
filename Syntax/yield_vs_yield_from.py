#!/usr/bin/python3
# -*- coding: utf8 -*-

def generator123() :
    yield 1
    yield 2
    yield 3

def callyield() :
    yield 4
    yield generator123()
    yield 5
    yield 6

def callyieldfrom() :
    yield 4
    yield from generator123()
    yield 5
    yield 6

def simpleyield() :
    yield generator123()

def simpleyieldfrom() :
    yield from generator123()

if __name__ == '__main__' :

    print("simple yield toss")
    for item in simpleyield() :
        print(item)
        l = list(item)
        print(l)
    print()

    print("simple yield from toss")
    for item in simpleyieldfrom() :
        print(item)
    print()

    print("yield")
    for item in callyield() :
        print(item)
    print()

    print("yield from")
    for item in callyieldfrom() :
        print(item)
    pass