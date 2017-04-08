#!/usr/bin/python3
# -*- coding: utf8 -*-

from collections import deque
from heapq import heappop, heappush, nsmallest

if __name__ == '__main__' :

    #deque
    print('#deque')
    fifo = deque()
    fifo.append(1)
    fifo.append(2)
    fifo.append(3)
    print(fifo.popleft())
    print(fifo.pop())
    print()

    #heap
    print('#heap')
    a = []
    heappush(a, 5)
    heappush(a, 3)
    heappush(a, 7)
    heappush(a, 4)
    print(a)
    print("pop ", heappop(a))
    print(a)
    print("pop ", heappop(a))
    print(a)
    print("pop ", heappop(a))
    print(a)
    print("pop ", heappop(a))
    print(a)
