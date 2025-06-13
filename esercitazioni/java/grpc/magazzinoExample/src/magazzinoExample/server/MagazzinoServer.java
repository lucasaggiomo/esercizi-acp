package magazzinoExample.server;

import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import io.grpc.Server;
import io.grpc.Grpc;
import io.grpc.InsecureServerCredentials;

public class MagazzinoServer {
    private static final int CAPACITY = 5;

    public static void main(String[] args) {
        int port = 0;

        // instanzia il servicer
        MagazzinoServicer servicer = new MagazzinoServicer(CAPACITY);

        // instanzia il server
        ExecutorService executor = Executors.newFixedThreadPool(10);
        Server server = Grpc
                .newServerBuilderForPort(port, InsecureServerCredentials.create())
                .executor(executor)
                .addService(servicer)
                .build();

        // avvia il server
        try {
            server.start();
        } catch (IOException e) {
            e.printStackTrace();
        }

        port = server.getPort();

        System.out.println("[SERVER] In ascolto su " + port);

        // attende la terminazione del server
        try {
            server.awaitTermination();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
