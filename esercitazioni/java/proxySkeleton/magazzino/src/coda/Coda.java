package coda;

public interface Coda {
    public int preleva();

    public void deposita(int value);

    public int size();

    public int getCapacity();

    public boolean isFull();

    public boolean isEmpty();
}
