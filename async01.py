#!/usr/bin/python3
"""
dabeazley python: build your own async - timestamp 00:19:22
the time.sleep() calls are blocking and prevent anything else from running
how to address this blocking issue ?
add a method to class Scheduler that schedules work to be run in the future.
"""
import time
from collections import deque


class Scheduler:
    """ Scheduler class """
    def __init__(self):
        """ init work queue """
        self.work_queue = deque()
        # list/queue that will be sorted by shortest delay first
        self.future_work_sorted = []

    def work_queue_add(self, work_function):
        """ add functions to be run to work queue """
        self.work_queue.append(work_function)

    # add future work functionality
    def future_work_add(self, time_delay, func):
        # need to coordinate/manage time delay
        # can create a list that is sorted least delay (shortest) to most
        # delay (longest)
        #
        # deadline by when func needs to run
        # there is a better way to sort this, but this method will
        # work for now
        deadline = time.time() + time_delay
        self.future_work_sorted.append((deadline, func))
        self.future_work_sorted.sort()

    def run(self):
        """ run/execute function from work queue """
        # need to coordinate future work queue and work queue
        #
        # while there is a func in the work queue or there is a func in the
        # future work queue, 
        while self.work_queue or self.future_work_sorted:
            # if nothing in work queue to be run, pull func from future work
            # sorted with the least/shortest time delay value
            if not self.work_queue:
                # unpack tuple (deadline, func)
                deadline, func = self.future_work_sorted.pop(0)
                # figure out how long before the func needs to be run
                # (i.e., time delta)
                time_delta = deadline - time.time()
                # sleep until it's time for the func to run
                # then add the func to the work queue to be run
                if time_delta > 0:
                    time.sleep(time_delta)
                self.work_queue.append(func)

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
        # this time.sleep() is a blocking call
        # use a future work scheduler to get around this
        # future work scheduler that takes a time delay (i.e., 4) and a
        # target function to be run
        #
        # time.sleep(4)
        # sched.work_queue_add(lambda: countdown(n - 1))
        sched.future_work_add(4, lambda: countdown(n - 1))


def countup(stop):
    """
    doc string
    """
    def _internal_func(x):
        if x < stop:
            print("Up", x)
            # time.sleep(1)
            # sched.work_queue_add(lambda: _internal_func(x + 1))
            sched.future_work_add(1, lambda: _internal_func(x + 1))
    _internal_func(0)


sched.work_queue_add(lambda: countdown(5))
sched.work_queue_add(lambda: countup(20))
sched.run()