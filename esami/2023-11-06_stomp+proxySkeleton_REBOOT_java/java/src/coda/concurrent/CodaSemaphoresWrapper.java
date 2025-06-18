package coda.concurrent;

import java.util.concurrent.Semaphore;

import coda.ICoda;
import coda.CodaWrapper;
import coda.exceptions.CodaIsEmptyException;
import coda.exceptions.CodaIsFullException;

public class CodaSemaphoresWrapper<T> extends CodaWrapper<T> {

    private final Semaphore prodSemaphore;
    private final Semaphore consSemaphore;
    private final Semaphore prodMutex;
    private final Semaphore consMutex;

    public CodaSemaphoresWrapper(ICoda<T> coda) {
        super(coda);
        this.prodSemaphore = new Semaphore(coda.getCapacity());
        this.consSemaphore = new Semaphore(0);
        this.prodMutex = new Semaphore(1);
        this.consMutex = new Semaphore(1);
    }

    @Override
    public void push(T item) throws CodaIsFullException {
        try {
            prodSemaphore.acquire();
            prodMutex.acquire();
            coda.push(item);

        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            prodMutex.release();
        }

        consSemaphore.release();
    }

    @Override
    public T pop() throws CodaIsEmptyException {
        T item = null;

        try {
            consSemaphore.acquire();
            consMutex.acquire();
            item = coda.pop();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            consMutex.release();
        }

        prodSemaphore.release();

        return item;
    }

}
