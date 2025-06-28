package coda;

public interface ICoda {
    public int preleva();

    public void deposita(int item);

    public int size();

    public boolean isFull();

    public boolean isEmpty();
}
