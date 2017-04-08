#!/usr/bin/python3
# -*- coding: utf8 -*-

import timeit

if __name__ == '__main__' :

    #basic __slots__

    class MyClass(object) :
        __slots__ = ('x', 'y')
        def __init__(self, *args, **kwargs) :
            self.x = 1
            self.y = 2

    #error 
    #print(a.__dict__)
    a = MyClass()
    print(a.__slots__)
    print(a.x, a.y)
    # no __dict__ not allow below
    #a.z = 10
        
    '''
    add __dict__ to __slot__
    '''

    class MyClassWithDict(object) :
        __slots__ = ('x', 'y', '__dict__') 
        def __init__(self, *args, **kwargs) :
            self.x = 1
            self.y = 2
    a = MyClassWithDict()
                      
    print(a.__dict__)
    print(a.__slots__)
    print(a.x, a.y)
    a.z = 10
    print(a.z)

    '''
    usage of slot
        1. faster attribute access
        2. potential space saving in memory
            ! __slot__ doesn't have __dict__ so small object which has few variables can save space
    '''

    class Foo(object) :
        __slots__ = ('foo')

    class Bar(object) :
        pass

    slotted = Foo()
    not_slotted = Bar()

    def get_set_delete_fn(obj) :
        def get_set_delete() :
            obj.foo = 'foo'
            obj.foo
            del obj.foo
        return get_set_delete

    print(min(timeit.repeat(get_set_delete_fn(slotted))))
    print(min(timeit.repeat(get_set_delete_fn(not_slotted))))
        