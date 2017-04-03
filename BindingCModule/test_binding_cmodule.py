#!/usr/bin/python3
# -*- coding: utf8 -*-

import myLib
import spam
from circle import Circle

'''
    if cannot import package check below (all pyd file goes to) path
        (C:\Python27)\Lib\site-packages\
'''

if __name__ == '__main__' :
    beginMsg = "c binding moduel logging test begin"
    endMsg = "c binding moduel logging test end"

    myLib.wlog(beginMsg)

    print(spam.strlen(beginMsg))
    print(spam.strlen(endMsg))

    num1 = 14
    num2 = 3
    print(spam.division(num1, num2))

    color = "white"
    radius = 10
    shape = Circle(color, radius)
    print(type(shape))
    print("color ", shape.color())
    print("area ", shape.area())

    myLib.wlog(endMsg)
