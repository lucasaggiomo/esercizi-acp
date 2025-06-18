package laptopService.user;

import java.util.Random;
import java.util.concurrent.TimeUnit;

import io.grpc.Grpc;
import io.grpc.InsecureChannelCredentials;
import io.grpc.ManagedChannel;
import laptopService.grpc.LaptopServiceGrpc;
import laptopService.grpc.LaptopServiceGrpc.LaptopServiceBlockingStub;

public class User {

    private static final int NUM_RICHIESTE = 10;

    private static final Random rand = new Random();

    public static void main(String[] args) {
        String host = null;
        int port = -1;

        try {
            if (args.length == 1) {
                host = "localhost";
                port = Integer.parseInt(args[0]);
            } else {
                host = args[0];
                port = Integer.parseInt(args[1]);
            }
        } catch (IndexOutOfBoundsException | NumberFormatException e) {
            System.out.println("Inserisci porta (default host = 'localhost') oppure host e porta del server");
            System.exit(1);
        }

        ManagedChannel channel = Grpc.newChannelBuilderForAddress(host, port, InsecureChannelCredentials.create())
                .build();
        LaptopServiceBlockingStub laptopService = LaptopServiceGrpc.newBlockingStub(channel);

        System.out.printf("[USER] Sono connesso, invio %d richieste...\n", NUM_RICHIESTE);

        Thread[] threads = new Thread[NUM_RICHIESTE];
        for (int i = 0; i < NUM_RICHIESTE; i++) {
            TipoRichiesta tipo = null;
            int serial_number = -1;
            if (i % 2 == 0) {
                tipo = TipoRichiesta.ACQUISTO;
            } else {
                tipo = TipoRichiesta.VENDITA;
                serial_number = 1 + rand.nextInt(100);
            }
            threads[i] = new UserThread(Integer.toString(i), laptopService, tipo, serial_number);
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
        try {
            channel.shutdownNow().awaitTermination(60, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

}
