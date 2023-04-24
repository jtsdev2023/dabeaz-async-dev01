#!/usr/bin/python3
"""
dabeazley python: build your own async - timestamp 00:26:15
the time.sleep() calls are blocking and prevent anything else from running
how to address this blocking issue ?
add a method to class Scheduler that schedules work to be run in the future.
"""
import time
from collections import deque


class Scheduler:
    def __init__(self):
        self.work_queue = deque()
        self.future_work_queue = []

    def work_queue_add(self, work_function):
        self.work_queue.append(work_function)
    
    def future_work_queue_add(self, hold_delay, work_function):
        target_run_time = time.time() + hold_delay
        self.future_work_queue.append((target_run_time, work_function))
        self.future_work_queue.sort()

    def run(self):
        while self.work_queue or self.future_work_queue:
            if not self.work_queue:
                target_run_time, work_function = self.future_work_queue.pop(0)
                hold_wait = target_run_time - time.time()
                if hold_wait > 0:
                    time.sleep(hold_wait)
                self.work_queue.append(work_function)
            while self.work_queue:
                work_function = self.work_queue.popleft()
                work_function()


work_scheduler = Scheduler()


def countdown(n):
    if n > 0:
        print('Count Down: ', n)
        work_scheduler.future_work_queue_add(4, lambda: countdown(n-1))


def countup(stop_count):
    def _internal_control_func(x):
        if x < stop_count:
            print('Count Up: ', x)
            work_scheduler.future_work_queue_add(
                1, lambda: _internal_control_func(x+1)
                )
    _internal_control_func(0)


work_scheduler.work_queue_add(lambda: countdown(5))
work_scheduler.work_queue_add(lambda: countup(20))
work_scheduler.run()
