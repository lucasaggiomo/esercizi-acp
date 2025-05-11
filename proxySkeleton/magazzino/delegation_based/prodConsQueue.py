import threading as th


class Queue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = [0] * capacity  # visto come array [0, 0, 0, 0]
        self.len = 0
        self.head = 0
        self.tail = 0

        # produttore e consumatore
        lock = th.Lock()
        self.prodCV = th.Condition(lock)
        self.consCV = th.Condition(lock)

    def produce(self, item):

        # self.prodCV.acquire()

        with self.prodCV:
            while self.len == self.capacity:
                self.prodCV.wait()

            self.buffer[self.head] = item
            self.head = (self.head + 1) % self.capacity
            self.len += 1

            self.consCV.notify()

        # self.prodCV.release()

    def consume(self):
        with self.consCV:
            while self.len == 0:
                self.consCV.wait()

            item = self.buffer[self.tail]
            self.tail = (self.tail + 1) % self.capacity
            self.len -= 1

            self.prodCV.notify()

        return item

    def __len__(self) -> int:
        return self.len
