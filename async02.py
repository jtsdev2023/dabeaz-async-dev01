#!/home/user01/py_venv/paramiko-async-dev01/bin/python
"""
DA Beazley async
"""

import time


# def countdown(n):
#     """
#     doc string
#     """
#     while n > 0:
#         print("Down", n)
#         time.sleep(1)
#         n -= 1


# def countup(stop):
#     """
#     doc string
#     """
#     x = 0
#     while x < stop:
#         print("Up", x)
#         time.sleep(1)
#         x += 1


# sequential execution
# countdown(5)
# countup(5)

# concurrent execution
# classic solution: use threads

# import threading


# threading.Thread(target=countdown, args=(5,)).start()
# threading.Thread(target=countup, args=(5,)).start()


# how can we do "concurrency" w/o threading?
# solve a scaling problem.
# i.e., creating 10,000 threads could be undesireable
# so how can we scale concurrency to 10,000 w/o threading?
# issue: figure out how to switch between tasks
"""
gotta get rid of the looping.
so how to iterate through tasks and do concurrent work?
schedule callback/function calls.
"""

from collections import deque

class Scheduler:
    def __init__(self):
        self.ready = deque()                # a queue of functions ready to execute

    def call_soon(self, func):
        self.ready.append(func)             # add functions to queue
    
    def run(self):
        while self.ready:
            func = self.ready.popleft()      # take functions out of queue and run them
            func()

sched = Scheduler()

def countdown(n):
    """
    doc string
    """
    if n > 0:
        print("Down", n)
        time.sleep(1)
        sched.call_soon(lambda: countdown(n - 1))


def countup(stop, x=0):
    """
    doc string
    """
    if x < stop:
        print("Up", x)
        time.sleep(1)
        sched.call_soon(lambda: countup(stop, x + 1))


sched.call_soon(lambda: countdown(5))
sched.call_soon(lambda: countup(5))
sched.run()
