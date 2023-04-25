#!/usr/bin/python3
"""
dabeazley python: build your own async - timestamp 00:36:18
how to do producer/consumer without queue and threading ?
how to incorporate the "class CustomScheduler" developed earlier ?
"""


import time
import heapq
from collections import deque


class CustomScheduler:
    """
    """
    def __init__(self):
        self.work_queue = deque()
        self.future_work_queue = []
        self.sequence_number = 0
    
    def work_queue_add(self, work_function):
        self.work_queue.append(work_function)
    
    def future_work_queue_add(self, hold_delay, work_function):
        target_execution_time = time.time() + hold_delay
        heapq.heappush(
            self.future_work_queue,
            (target_execution_time, self.sequence_number, work_function)
            )
        self.sequence_number += 1
    
    def run(self):
        while self.work_queue or self.future_work_queue:
            if not self.work_queue:
                target_execution_time, _, work_function = \
                heapq.heappop(self.future_work_queue)
                hold_wait = target_execution_time - time.time()
                if hold_wait > 0:
                    time.sleep(hold_wait)
                self.work_queue.append(work_function)
            while self.work_queue:
                work_function = self.work_queue.popleft()
                work_function()


work_scheduler = CustomScheduler()


class CustomAsyncQueue:
    """
    """
    def __init__(self):
        self.items = deque()
        self.waiting = deque()

    def put(self, item):
        self.items.append(item)
        if self.waiting:
            func = self.waiting.popleft()
            work_scheduler.work_queue_add(func)


    def get(self, callback_method):
        if self.items:
            callback_method(self.items.popleft())
        else:
            self.waiting.append(lambda: self.get(callback_method))


def producer(queue, count):
    def _internal_control_func(n):
        if n < count:
            print('Producing: ', n)
            q.put(n)
            work_scheduler.future_work_queue_add(
                1, lambda: _internal_control_func(n+1)
            )
        else:
            print('Producing --> Done')
            q.put(None)
    _internal_control_func(0)


def consumer(q):
    def _consume(item):
        if item is None:
            print('Consumer --> Done')
        else:
            print('Consuming: ', item)
            work_scheduler.work_queue_add(lambda: consumer(q))
    q.get(callback_method=_consume)


q = CustomAsyncQueue()
work_scheduler.work_queue_add(lambda: producer(q, 10))
work_scheduler.work_queue_add(lambda: consumer(q,))
work_scheduler.run()
