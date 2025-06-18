import threading as th
from queues.queue import IQueue
from queues.queueWrapper import QueueWrapper


class CodaProdCons(QueueWrapper):
    def __init__(self, queue: IQueue):
        super().__init__(queue)
        self.lock = th.Lock()
        self.prodCV = th.Condition(self.lock)
        self.consCV = th.Condition(self.lock)

    def push(self, item):
        with self.prodCV:
            while self.queue.isFull():
                self.prodCV.wait()

            self.queue.push(item)

            self.consCV.notify()

    def pop(self):
        with self.consCV:
            while self.queue.isEmpty():
                self.consCV.wait()

            item = self.queue.pop()

            self.prodCV.notify()

        return item
