package coda;

import coda.exceptions.CodaIsEmptyException;
import coda.exceptions.CodaIsFullException;

public interface ICoda<T> {

    public void push(T item) throws CodaIsFullException;

    public T pop() throws CodaIsEmptyException;

    public boolean isEmpty();

    public boolean isFull();

    public int size();

    public int getCapacity();

}
