package magazzino.server;

import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import coda.CodaProdCons;
import coda.ICoda;

import io.grpc.Grpc;
import io.grpc.InsecureServerCredentials;
import io.grpc.Server;

public class MagazzinoServer {

    private static final int DIM_CODA = 5;

    private static int PORT = 0;

    public static void main(String[] args) {
        ICoda coda = new CodaProdCons(DIM_CODA);

        MagazzinoServicerImpl servicer = new MagazzinoServicerImpl(coda);

        ExecutorService executor = Executors.newFixedThreadPool(2);
        Server server = Grpc.newServerBuilderForPort(PORT, InsecureServerCredentials.create())
                .executor(executor)
                .addService(servicer)
                .build();

        try {
            server.start();
            PORT = server.getPort();
            System.out.printf("[SERVER] In attesa sulla porta %s\n", PORT);

            try {
                server.awaitTermination();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
