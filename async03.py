#!/usr/bin/python3
""" dabeazley python: build your own async - timestamp 13:13"""
import time
from collections import deque


class Scheduler:
    """ Scheduler class """
    def __init__(self):
        """ init work queue """
        self.work_queue = deque()

    def work_queue_add(self, work_function):
        """ add functions to be run to work queue """
        self.work_queue.append(work_function)

    def run(self):
        """ run/execute function from work queue """
        while self.work_queue:
            func = self.work_queue.popleft()
            func()


sched = Scheduler()


def countdown(n):
    """
    doc string
    """
    if n > 0:
        print("Down", n)
        time.sleep(1)
        sched.work_queue_add(lambda: countdown(n - 1))


def countup(stop, x=0):
    """
    doc string
    """
    if x < stop:
        print("Up", x)
        time.sleep(1)
        sched.work_queue_add(lambda: countup(stop, x + 1))


sched.work_queue_add(lambda: countdown(5))
sched.work_queue_add(lambda: countup(5))
sched.run()