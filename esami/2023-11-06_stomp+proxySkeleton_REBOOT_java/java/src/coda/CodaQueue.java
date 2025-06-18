package coda;

import java.util.PriorityQueue;
import java.util.Queue;

import coda.exceptions.CodaIsEmptyException;
import coda.exceptions.CodaIsFullException;

public class CodaQueue<T> implements ICoda<T> {
    private final Queue<T> queue;
    private final int capacity;

    public CodaQueue(int capacity) {
        super();
        this.queue = new PriorityQueue<>(capacity);
        this.capacity = capacity;
    }

    @Override
    public void push(T item) throws CodaIsFullException {
        if (queue.size() == capacity)
            throw new CodaIsFullException("Tentativo di push con coda piena");

        queue.add(item);
    }

    @Override
    public T pop() throws CodaIsEmptyException {
        if (queue.size() == 0)
            throw new CodaIsEmptyException("Tentativo di pop con coda piena");

        return queue.remove();
    }

    @Override
    public boolean isEmpty() {
        return queue.isEmpty();
    }

    @Override
    public boolean isFull() {
        return queue.size() == capacity;
    }

    @Override
    public int size() {
        return queue.size();
    }

    @Override
    public int getCapacity() {
        return capacity;
    }
}
