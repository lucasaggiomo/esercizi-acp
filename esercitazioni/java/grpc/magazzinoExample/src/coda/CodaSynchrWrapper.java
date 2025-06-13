package coda;

public class CodaSynchrWrapper<T> extends CodaWrapper<T> {

    public CodaSynchrWrapper(Coda<T> coda) {
        super(coda);
    }

    @Override
    public void push(T item) throws CodaIsFullException {
        synchronized (coda) {
            while (coda.isFull()) {
                try {
                    coda.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            coda.push(item);

            coda.notifyAll();
        }
    }

    @Override
    public T pop() throws CodaIsEmptyException {
        synchronized (coda) {
            while (coda.isEmpty()) {
                try {
                    coda.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            T item = coda.pop();

            coda.notifyAll();

            return item;
        }
    }

}
