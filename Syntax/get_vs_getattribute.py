#!/usr/bin/python3
# -*- coding: utf8 -*-

class LoggingAccess(object) :
    def __init__(self) :
        self.value = 0;
        print('LoggingAccess create')

    def __get__(self, intance, owner) :
        print('__get__', intance, owner)
        return self.value

    def __set__(self, instance, value) :
        print('__set__', instance, value)
        self.value = value

    def __setattr__(self, attr, value):
        print('__setattr__', attr, value)
        return super().__setattr__(attr, value)

    def __getattr__(self, attr) :
        '''def __getattribute__(self, attr) doesn't found match return None'''
        print('__getattr__', attr)
        return None

    def __getattribute__(self, attr) :
        print('__getattribute__', attr)
        return super().__getattribute__(attr)

class DescriptorAccess(object) :
    desc = LoggingAccess()

if __name__ == '__main__' :
    logObj = LoggingAccess()
    descObj = DescriptorAccess()

    #print(logObj.__dict__)
    #print(descObj.__dict__)

    print()
    print('#test LoggingAccess')

    print(logObj.v)
    logObj.value = 1
    print(logObj.value)
    print()
    LoggingAccess.__setattr__(logObj, 'v', 2)
    print(LoggingAccess.__getattribute__(logObj, 'v'))

    print()
    print('#test LoggingAccess')

    descObj.desc = 1
    print(descObj.desc)
    print()

    print(DescriptorAccess.__dict__['desc'])
    '''
        @descriptor protocol

            descr.__get__(self, obj, type=None) --> value
            descr.__set__(self, obj, value) --> None
            descr.__delete__(self, obj) --> None
    '''
    LoggingAccess.__set__(descObj, descObj, 2)
    print(LoggingAccess.__get__(descObj, descObj, descObj))
    
    DescriptorAccess.__dict__['desc'].__set__(descObj, 3)
    print(DescriptorAccess.__dict__['desc'].__get__(descObj, DescriptorAccess))

    