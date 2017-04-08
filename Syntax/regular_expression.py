#!/usr/bin/python3
# -*- coding: utf8 -*-

import re
from pprint import pprint

if __name__ == '__main__' :
    
    quationSpliter = re.compile('[\'\"]')
    text = r'<PropertyGroup Condition="\'$(Configuration)|$(Platform)\'==\'Debug|Win32\'" Label="Configuration">'

    #split
    print('#split')
    splitList = quationSpliter.split(text)
    pprint(splitList)

    #sub
    print('#sub')
    subList = quationSpliter.sub('\^\^', text)
    pprint(subList)
    
    data = """
    park 800905-1049118
    kim  700905-1059119
    """
    
    pat = re.compile("(\d{6})[-]\d{7}")
    print(pat.sub("\g<1>-*******", data))

    #findall
    print('#findall')
    findallList = pat.findall(data)
    print(findallList)