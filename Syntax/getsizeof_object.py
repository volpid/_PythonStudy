#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys

class Temp(object) :
    def __init__(self) :
        self.a = []
        self.b = {}

if __name__ == '__main__' :
    
    i = 1
    s = "string"
    empty_list = []
    item_list = [1, 2, "nan"]
    empty_dict = {}
    item_dict = {1:1, 2:2, 3:"nan"}
    obj = object()
    ldObj = Temp()
    
    print("i", sys.getsizeof(i));
    print("s", sys.getsizeof(s));
    print("empty_list", sys.getsizeof(empty_list));
    print("item_list", sys.getsizeof(item_list));
    print("empty_dict", sys.getsizeof(empty_dict));
    print("item_dict", sys.getsizeof(item_dict));
    print("obj", sys.getsizeof(obj));
    print("ldObj", sys.getsizeof(ldObj));
    print("ldObj.a", sys.getsizeof(ldObj.a));
    print("ldObj.b", sys.getsizeof(ldObj.b));
