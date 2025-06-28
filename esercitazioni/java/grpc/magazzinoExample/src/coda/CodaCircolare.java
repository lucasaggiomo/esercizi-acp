package coda;

import java.util.ArrayList;
import java.util.List;

public class CodaCircolare<T> implements Coda<T> {
    private final int capacity;
    private final List<T> buffer;

    private int testa;
    private int coda;
    private int size;

    public CodaCircolare(int capacity) {
        this.capacity = capacity;
        this.buffer = new ArrayList<T>(capacity);
        for (int i = 0; i < capacity; i++) {
            buffer.add(null);
        }
        this.testa = 0;
        this.coda = 0;
        this.size = 0;
    }

    @Override
    public void push(T item) throws CodaIsFullException {
        if (size == capacity)
            throw new CodaIsFullException("Tentativo di push con coda piena");

        this.buffer.set(testa, item);
        testa = (testa + 1) % capacity;
        size++;
    }

    @Override
    public T pop() throws CodaIsEmptyException {
        if (size == 0)
            throw new CodaIsEmptyException("Tentativo di pop con coda piena");

        T item = this.buffer.get(coda);
        coda = (coda + 1) % capacity;
        size--;
        return item;
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
    }

    @Override
    public boolean isFull() {
        return size == capacity;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public int getCapacity() {
        return capacity;
    }

}
