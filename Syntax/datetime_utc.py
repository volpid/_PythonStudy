#!/usr/bin/python3
# -*- coding: utf8 -*-

from datetime import datetime, timezone
from time import mktime, strptime

if __name__ == '__main__' :
    
    #datetime to utc
    now = datetime(2017, 4, 12, 20, 20)
    now = now.replace(tzinfo = timezone.utc)
    now_time_tuple = now.timetuple()
    utc_now = mktime(now_time_tuple)
    
    print(utc_now)
    print(now_time_tuple)
    print(now)
    print(now.astimezone())