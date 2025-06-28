package coda;

public abstract class CodaWrapper implements Coda {
    protected final Coda coda;

    public CodaWrapper(Coda coda) {
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
