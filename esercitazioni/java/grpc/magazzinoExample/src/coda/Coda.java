package coda;

public interface Coda<T> {

    public void push(T item) throws CodaIsFullException;

    public T pop() throws CodaIsEmptyException;

    public boolean isEmpty();

    public boolean isFull();

    public int size();

    public int getCapacity();

}
