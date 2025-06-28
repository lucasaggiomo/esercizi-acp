import multiprocessing as mp


# NOTE: Ogni processo necessita di una sua StatsQueue locale, a cui deve essere passata
# la stessa coda multiprocessing.Queue e gli stessi lock / variabili condition
class StatsQueue:
    def __init__(self, queue: mp.Queue, prodCV: mp.Condition, consCV: mp.Condition):
        self.queue = queue
        self.prodCV = prodCV
        self.consCV = consCV

    def push(self, item):
        with self.prodCV:
            while self.queue.full():
                self.prodCV.wait()

            self.queue.put(item)

            self.consCV.notify()

    def pop(self):
        with self.consCV:
            while self.queue.empty():
                self.consCV.wait()

            item = self.queue.get()

            self.prodCV.notify()

        return item

    def svuota(self):
        items = []
        with self.consCV:
            while not self.queue.empty():
                items.append(self.queue.get())

            self.prodCV.notify_all()

        return items

    def isEmpty(self):
        return self.queue.empty()

    def isFull(self):
        return self.queue.full()
