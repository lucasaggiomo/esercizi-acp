from typing import Any

from queues.queue import IQueue


class CircularQueue(IQueue):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = [None for _ in range(self.capacity)]
        self.size = 0
        self.testa = 0
        self.coda = 0

    def push(self, item: Any) -> None:
        self.buffer[self.testa] = item
        self.testa = (self.testa + 1) % self.capacity
        self.size += 1

    def pop(self) -> Any:
        item = self.buffer[self.coda]
        self.coda = (self.coda + 1) % self.capacity
        self.size -= 1
        return item

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity

    def __len__(self) -> int:
        return self.size
