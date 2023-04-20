#!/home/user01/py_venv/paramiko-async-dev01/bin/python
"""
DA Beazley async
"""

import time


def countdown(n):
    """
    doc string
    """
    while n > 0:
        print("Down", n)
        time.sleep(1)
        n -= 1


def countup(stop):
    """
    doc string
    """
    x = 0
    while x < stop:
        print("Up", x)
        time.sleep(1)
        x += 1


# sequential execution
countdown(5)
countup(5)
