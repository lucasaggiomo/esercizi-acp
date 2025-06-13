package coda;

public abstract class CodaWrapper<T> implements Coda<T> {

    protected Coda<T> coda;

    public CodaWrapper(Coda<T> coda) {
        this.coda = coda;
    }

    @Override
    public boolean isEmpty() {
        return coda.isEmpty();
    }

    @Override
    public boolean isFull() {
        return coda.isFull();
    }

    @Override
    public int size() {
        return coda.size();
    }

    @Override
    public int getCapacity() {
        return coda.getCapacity();
    }

}
