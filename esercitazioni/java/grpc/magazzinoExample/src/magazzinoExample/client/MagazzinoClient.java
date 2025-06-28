package magazzinoExample.client;

import java.util.Random;
import java.util.concurrent.TimeUnit;

import magazzinoExample.magazzino.Acknowledge;
import magazzinoExample.magazzino.Articolo;
import magazzinoExample.magazzino.Empty;
import magazzinoExample.magazzino.MagazzinoGrpc;
import magazzinoExample.magazzino.MagazzinoGrpc.MagazzinoBlockingStub;
import io.grpc.Grpc;
import io.grpc.InsecureChannelCredentials;
import io.grpc.ManagedChannel;
import io.grpc.StatusRuntimeException;

public class MagazzinoClient {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Inserisci il numero di porta");
            System.exit(1);
            return;
        }

        int port = Integer.parseInt(args[0]);
        // creo il canale di connessione verso il server
        ManagedChannel channel = Grpc
                .newChannelBuilderForAddress("localhost", port, InsecureChannelCredentials.create()).build();

        // crea lo stub
        MagazzinoBlockingStub magazzinoBlockingStub = MagazzinoGrpc.newBlockingStub(channel);

        Random rand = new Random();

        // effettua le richieste
        try {
            for (int i = 0; i < 10; i++) {
                if (i % 2 == 0) {

                    long id = rand.nextInt(1, 100);
                    Articolo articolo = Articolo.newBuilder().setId(id).build();

                    System.out.println("[CLIENT] Deposito " + id);
                    Acknowledge ack = magazzinoBlockingStub.deposita(articolo);
                    System.out.println("[CLIENT] Ricevuto " + ack.getMessage());

                } else {

                    Empty empty = Empty.newBuilder().build();

                    System.out.println("[CLIENT] Prelevo");
                    Articolo articolo = magazzinoBlockingStub.preleva(empty);
                    long id = articolo.getId();
                    System.out.println("[CLIENT] Ricevuto " + id);

                }
            }
        } catch (StatusRuntimeException e) {
            System.out.println("Errore di grpc: " + e.getStatus());
            e.printStackTrace();
        }

        // chiude il canale
        try {
            channel.shutdownNow().awaitTermination(10, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
