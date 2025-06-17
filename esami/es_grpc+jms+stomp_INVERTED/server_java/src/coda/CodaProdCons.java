package coda;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class CodaProdCons implements ICoda {
    private final int capacity;
    private int size;
    private int testa;
    private int coda;
    private final Lock lock;
    private final Condition prodCV;
    private final Condition consCV;
    private final int[] buffer;

    public CodaProdCons(int capacity) {
        this.capacity = capacity;
        this.size = 0;
        this.testa = 0;
        this.coda = 0;
        this.buffer = new int[capacity];

        this.lock = new ReentrantLock();
        this.prodCV = lock.newCondition();
        this.consCV = lock.newCondition();
    }

    public void deposita(int item) {

        try {
            lock.lock();

            while (size == capacity) {
                try {
                    prodCV.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            buffer[testa] = item;
            testa = (testa + 1) % capacity;
            size += 1;

            consCV.signal();
        } finally {
            lock.unlock();
        }

    }

    public int preleva() {

        int item = -1;

        try {
            lock.lock();

            while (size == 0) {
                try {
                    consCV.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            item = buffer[coda];
            coda = (coda + 1) % capacity;
            size -= 1;

            prodCV.signal();
        } finally {
            lock.unlock();
        }

        return item;

    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public boolean isFull() {
        return size == capacity;
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
    }
}
