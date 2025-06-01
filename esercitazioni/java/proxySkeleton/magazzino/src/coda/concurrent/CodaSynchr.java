package coda.concurrent;

import coda.Coda;
import coda.CodaWrapper;

public class CodaSynchr extends CodaWrapper {

    public CodaSynchr(Coda coda) {
        super(coda);
    }

    @Override
    public int preleva() {
        int output = -1;
        synchronized (coda) {
            while (coda.isEmpty()) {
                try {
                    coda.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            output = coda.preleva();

            coda.notifyAll();
        }
        return output;
    }

    @Override
    public void deposita(int value) {
        synchronized (coda) {
            while (coda.isFull()) {
                try {
                    coda.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            coda.deposita(value);

            coda.notifyAll();
        }
    }

}
