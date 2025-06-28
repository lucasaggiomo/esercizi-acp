from typing import Any
import abc

from queues.queue import IQueue


class QueueWrapper(IQueue):
    def __init__(self, queue: IQueue):
        self.queue = queue

    @abc.abstractmethod
    def push(self, item: Any) -> None:
        pass

    @abc.abstractmethod
    def pop(self) -> Any:
        pass

    def isEmpty(self) -> bool:
        return self.queue.isEmpty()

    def isFull(self) -> bool:
        return self.queue.isFull()

    def __len__(self) -> int:
        return len(self.queue)
