import abc


class IQueue(abc.ABC):
    @abc.abstractmethod
    def push(self, item):
        pass

    @abc.abstractmethod
    def pop(self):
        pass

    @abc.abstractmethod
    def isEmpty(self) -> bool:
        pass

    @abc.abstractmethod
    def isFull(self) -> bool:
        pass

    @abc.abstractmethod
    def __len__(self) -> int:
        pass
