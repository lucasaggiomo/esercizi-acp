package coda.impl;

import coda.Coda;

public class CodaCircolare implements Coda {
    private final int[] buffer;
    private int testa;
    private int coda;
    private int size;

    public CodaCircolare(int capacity) {
        this.buffer = new int[capacity];
        this.testa = 0;
        this.coda = 0;
        this.size = 0;
    }

    public int preleva() {
        size++;
        return buffer[testa++ % buffer.length];
    }

    public void deposita(int value) {
        size--;
        buffer[coda++ % buffer.length] = value;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public boolean isFull() {
        return size == buffer.length;
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
    }

    @Override
    public int getCapacity() {
        return buffer.length;
    }

}
