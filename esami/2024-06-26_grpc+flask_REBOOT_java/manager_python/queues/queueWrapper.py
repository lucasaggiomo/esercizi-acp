from queues.queue import IQueue


class QueueWrapper(IQueue):
    def __init__(self, queue: IQueue):
        self.queue = queue

    def isEmpty(self) -> bool:
        return self.queue.isEmpty()

    def isFull(self) -> bool:
        return self.queue.isFull()

    def __len__(self) -> int:
        return len(self.queue)
