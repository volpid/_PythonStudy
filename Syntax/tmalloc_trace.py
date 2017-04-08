#!/usr/bin/python3
# -*- coding: utf8 -*-

import gc
import tracemalloc

if __name__ == '__main__' :

    found_object = gc.get_objects()
    print('%d obj before' % len(found_object))
    for obj in found_object[:3] :
        print(repr(obj)[:100])
    found_object = gc.get_objects()
    print('%d obj after' % len(found_object))
    print()

    #tracemalloc
    tracemalloc.start(10)
    time1 = tracemalloc.take_snapshot()
    x = [1, 2, 3, 4, 5, 6]
    time2 = tracemalloc.take_snapshot()

    stats = time2.compare_to(time1, 'lineno')
    for stat in stats[:3] :
        print(stat)
    print()

    top = stats[0]
    print('\n'.join(top.traceback.format()))
