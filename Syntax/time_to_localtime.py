#!/usr/bin/python3
# -*- coding: utf8 -*-

from time import localtime, strftime

if __name__ == '__main__' :
    now = 1407694710

    local_tuple = localtime(now)
    time_format = '%Y-%m-%d %H:%M:%S'
    time_str = strftime(time_format, local_tuple)

    print(local_tuple)
    print()
    print(time_str)
