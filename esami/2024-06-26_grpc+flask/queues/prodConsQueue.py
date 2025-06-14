from typing import Any
import threading as th

from queues.queue import IQueue
from queues.queueWrapper import QueueWrapper


class ProdConsQueue(QueueWrapper):
    def __init__(self, queue: IQueue):
        super().__init__(queue)

        self.lock = th.Lock()
        self.prodCV = th.Condition(self.lock)
        self.consCV = th.Condition(self.lock)

    def push(self, item: Any) -> None:
        with self.lock:
            while self.queue.isFull():
                self.prodCV.wait()

            self.queue.push(item)

            self.consCV.notify()

    def pop(self) -> Any:
        with self.lock:
            while self.queue.isEmpty():
                self.consCV.wait()

            item = self.queue.pop()

            self.prodCV.notify()

        return item
