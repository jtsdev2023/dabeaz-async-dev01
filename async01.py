#!/usr/bin/python3
"""
dabeazley python: build your own async - timestamp 00:33:00
start producer/consumer
"""


import time
import queue
import threading


def producer(queue, count):
    for n in range(1, (count + 1)):
        print('Producing: ', n)
        q.put(n)
        time.sleep(1)
    
    print('Producing --> Done')
    q.put(None)


def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print('Consuming: ', item)
    print('Consumer --> Done')


q = queue.Queue()
threading.Thread(target=producer, args=(q, 10)).start()
threading.Thread(target=consumer, args=(q,)).start()