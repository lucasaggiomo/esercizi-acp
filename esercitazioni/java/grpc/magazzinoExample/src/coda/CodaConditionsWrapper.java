package coda;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class CodaConditionsWrapper<T> extends CodaWrapper<T> {

    private final Lock lock;
    private final Condition prodCondition;
    private final Condition consCondition;

    public CodaConditionsWrapper(Coda<T> coda) {
        super(coda);
        this.lock = new ReentrantLock();
        this.prodCondition = lock.newCondition();
        this.consCondition = lock.newCondition();
    }

    @Override
    public void push(T item) throws CodaIsFullException {
        lock.lock();

        try {
            while (coda.isFull()) {
                try {
                    prodCondition.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            coda.push(item);

            consCondition.signal();

        } finally {
            lock.unlock();
        }

    }

    @Override
    public T pop() throws CodaIsEmptyException {
        T item = null;

        lock.lock();

        try {
            while (coda.isEmpty()) {
                try {
                    consCondition.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            item = coda.pop();

            prodCondition.signal();
        } finally {
            lock.unlock();
        }

        return item;
    }

}
