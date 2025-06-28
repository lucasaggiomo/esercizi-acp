package client;

import java.util.Random;
import java.util.concurrent.TimeUnit;

import client.socket.TCP.MagazzinoProxySocketTCP;
import client.socket.UDP.MagazzinoProxySocketUDP;
import magazzino.Articolo;
import magazzino.IMagazzino;

public class ClientB {
    private final static int NUM_THREADS = 5;
    private final static int NUM_RICHIESTE = 3;

    public static class WorkingThread extends Thread {
        private IMagazzino magazzino;
        private int numRichieste;

        public WorkingThread(IMagazzino magazzino, int numRichieste) {
            super();
            this.magazzino = magazzino;
            this.numRichieste = numRichieste;
        }

        @Override
        public void run() {
            for (int i = 0; i < numRichieste; i++) {
                doStuff();
            }
        }

        private void doStuff() {
            Random rand = new Random();
            int secondsToSleep = rand.nextInt(2, 5);

            try {
                TimeUnit.SECONDS.sleep(secondsToSleep);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            int articoloIndex = rand.nextInt(Articolo.values().length);
            Articolo articolo = Articolo.values()[articoloIndex];

            System.out.printf("[CLIENT_B_THREAD - %s] Invio una richiesta di prelievo di un articolo %s\n",
                    this.getName(), articolo.name());
            int id = magazzino.preleva(articolo);
            System.out.printf("[CLIENT_B_THREAD - %s] Ho ricevuto l'id %d\n", this.getName(), id);
        }

    }

    public static void main(String[] args) {
        String host;
        int port;
        try {
            host = args[0];
            port = Integer.parseInt(args[1]);
        } catch (Exception e) {
            System.out.println("Inserisci l'host e il numero di porta del server");
            System.exit(-1);
            return;
        }

        IMagazzino magazzino = new MagazzinoProxySocketTCP(host, port);

        Thread[] threads = new Thread[NUM_THREADS];
        for (int i = 0; i < NUM_THREADS; i++) {
            threads[i] = new WorkingThread(magazzino, NUM_RICHIESTE);
            threads[i].setName(Integer.toString(i));
            threads[i].start();
        }

        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

    }
}
