package coda.concurrent;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import coda.Coda;
import coda.CodaWrapper;

public class CodaLock extends CodaWrapper {

    private final Lock lock;
    private final Condition cvProd;
    private final Condition cvCons;

    public CodaLock(Coda coda) {
        super(coda);
        lock = new ReentrantLock();
        cvProd = lock.newCondition();
        cvCons = lock.newCondition();
    }

    @Override
    public int preleva() {
        int output = -1;
        lock.lock();

        try {
            while (coda.isEmpty()) {
                try {
                    cvCons.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            output = coda.preleva();
            cvProd.signal();

        } finally {
            lock.unlock();
        }

        return output;
    }

    @Override
    public void deposita(int value) {
        lock.lock();

        try {
            while (coda.isFull()) {
                try {
                    cvProd.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            coda.deposita(value);
            cvCons.signal();

        } finally {
            lock.unlock();
        }
    }

}
