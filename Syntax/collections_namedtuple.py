#!/usr/bin/python3
# -*- coding: utf8 -*-

from collections import namedtuple

if __name__ == '__main__' :
    
    #namedtuple
    Coord2D = namedtuple('Coord2D', ('x', 'y'))
    Extend = namedtuple('Extend', 'z')
    Coord3D = namedtuple('Coord3D', Coord2D._fields + Extend._fields)

    a = Coord2D(1, 2)
    b = Coord3D(1, 2, '3')

    print('a[0], a[1]', a[0], a[1])
    print('b.x, b.y, b.z', b.x, b.y, b.z)
    print(a)
    print(str(b))

    l = [2, 3]
    d = {'y' : 4, 'z' : 'z', 'x' : 5}
    print(Coord2D._make(l))
    print(Coord2D(*l))
    print(Coord3D(**d))

    print(b._fields)