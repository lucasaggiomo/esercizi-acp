package coda.concurrent;

import java.util.concurrent.Semaphore;

import coda.Coda;
import coda.CodaWrapper;

public class CodaSemaphores extends CodaWrapper {

    private final Semaphore semCons;
    private final Semaphore semProd;

    // potrebbero essere anche lock, evitano a più consumatori / più produttori di
    // accedere alla coda sono due mutex separati, per garantire che i produttori
    // non blocchino i consumatori, qualora entrambi possano entrare (l'unica
    // risorsa che hanno in comune è size, che subisce operazioni atomiche di
    // incremento e decremento, mentre testa e coda sono sempre distinti, in quanto
    // gli altri semafori impediscono ad un consumatore di entrare se testa == coda,
    // in quanto significa size == 0)
    // utilizzando un solo mutex (o un blocco synchronized(coda)), comporterebbe
    // invece che un produttore e un consumatore non possono entrare
    // contemporaneamente anche quando potrebbero
    private final Semaphore mutexCons;
    private final Semaphore mutexProd;

    public CodaSemaphores(Coda coda) {
        super(coda);
        semCons = new Semaphore(0);
        semProd = new Semaphore(coda.getCapacity());
        mutexCons = new Semaphore(1);
        mutexProd = new Semaphore(1);
    }

    @Override
    public int preleva() {
        int output = -1;
        try {
            semCons.acquire();

            mutexCons.acquire();

            output = coda.preleva();

        } catch (InterruptedException e) {
            e.printStackTrace();

        } finally {
            mutexCons.release();
        }

        semProd.release();
        return output;
    }

    @Override
    public void deposita(int value) {
        try {
            semProd.acquire();

            mutexProd.acquire();

            coda.deposita(value);

        } catch (InterruptedException e) {
            e.printStackTrace();

        } finally {
            mutexProd.release();
        }

        semCons.release();
    }

}
