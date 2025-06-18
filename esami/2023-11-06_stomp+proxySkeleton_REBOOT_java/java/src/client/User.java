package client;

import java.util.Random;

import printer.TipoStampa;
import printer.proxy.IPrinterProxyFactory;
import printer.proxy.PrinterProxyFactoryTCP;
import printer.proxy.PrinterProxyFactoryUDP;

public class User {

    private static final int NUM_STAMPE = 10;

    private static final Random rand = new Random();

    private static <T> T getRandomElement(T[] array) {
        return array[rand.nextInt(array.length)];
    }

    private static final String[] estensioniValide = new String[] { "doc", "txt" };

    public static void main(String[] args) {
        final String HOST;
        final int PORT;
        try {
            if (args.length == 1) {
                HOST = "localhost";
                PORT = Integer.parseInt(args[0]);
            } else {
                HOST = args[0];
                PORT = Integer.parseInt(args[1]);
            }
        } catch (IndexOutOfBoundsException | NumberFormatException e) {
            System.out.println(
                    "Inserisci il numero di porta del server (default host = 'localhost'), oppure l'host seguito dal numero di porta");
            System.exit(1);
            return; // ridondante, per rimuovere il warning di HOST e PORT non inizializzate
        }

        IPrinterProxyFactory proxyFactory = new PrinterProxyFactoryUDP();

        // Il Client genera 10 richieste di stampa, invocando il metodo print per ogni
        // richiesta (attendendo 1 secondo tra le invocazioni). Per ciascuna richiesta,
        // tipo è generato in maniera casuale scegliendo tra bw, gs e color, mentre
        // pathFile è generato in maniera casuale, come /user/file_{NUM}.{estensione},
        // dove {NUM} è un valore numerico scelto casualmente tra 0 e 100, ed estensione
        // è una stringa scelta a caso tra doc e txt

        System.out.printf("[USER] Effettuo %d stampe...\n", NUM_STAMPE);
        Thread[] threads = new Thread[NUM_STAMPE];

        for (int i = 0; i < NUM_STAMPE; i++) {
            int numeroFile = rand.nextInt(101);
            String estensioneFile = getRandomElement(estensioniValide);
            String pathFile = String.format("/user/file_%d.%s", numeroFile, estensioneFile);
            TipoStampa tipo = getRandomElement(TipoStampa.values());

            threads[i] = new UserThread(Integer.toString(i), HOST, PORT, proxyFactory, pathFile, tipo);
            threads[i].start();

            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        for (Thread t : threads) {
            try {
                t.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        System.out.println("[USER] Termino...");

    }
}
