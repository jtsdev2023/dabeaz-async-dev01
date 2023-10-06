# scratch01.py


# Build Your Own Async
#
# David Beazley (@dabeaz)
# https://www.dabeaz.com
#
# Originally presented at PyCon India, Chennai, October 14, 2019

import time
from collections import deque


class Scheduler:
    """doc string"""
    def __init__(self) -> None:
        self.ready = deque()

    def current_work(self, input_funct: object) -> None:
        """doc string"""
        self.ready.append((input_funct))

    def run(self) -> None:
        """doc string"""
        while self.ready:
            _funct = self.ready.popleft()
            _funct()


sched = Scheduler()

# the way countdown() and countup() are structered with the conditional "if"
# behaves essentially like a "while" loop
def countdown(n: float) -> None:
    """doc string"""
    if n > 0:
        print('Down', n)
        time.sleep(1)
        sched.current_work(lambda: countdown(n-1))      # callback: countdown calling itself



def countup(stop: float) -> None:
    """doc string"""
    def _run(x):
        if x <= stop:
            print('Up', x)
            time.sleep(1)
            sched.current_work(lambda: _run(x+1))

    _run(1)


sched.current_work(lambda: countdown(5))
sched.current_work(lambda: countup(5))
sched.run()
