import time
from collections import deque


class Scheduler:
    def __init__(self):
        self.work_queue = deque()
    def queue_work(self, work_function):
        self.work_queue.append(work_function)
    def run(self):
        while self.work_queue:
            func = self.work_queue.popleft()
            func()


def test1(input_str):
    print(input_str)

def test2(input_str):
    print(input_str)

s = Scheduler()
s.queue_work(lambda: test1('one'))
s.queue_work(lambda: test2('two'))
s.run()
