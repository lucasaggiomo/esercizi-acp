from queues.queue import IQueue


class CodaCircolare(IQueue):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.testa = 0
        self.coda = 0
        self.size = 0

    def push(self, item):
        self.buffer[self.testa] = item
        self.testa = (self.testa + 1) % self.capacity
        self.size += 1

    def pop(self):
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
