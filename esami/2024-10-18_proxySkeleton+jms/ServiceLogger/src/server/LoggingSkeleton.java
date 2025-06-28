package server;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

import logging.ILogging;

public abstract class LoggingSkeleton implements ILogging {
    private int port;

    public LoggingSkeleton(int port) {
        this.port = port;
    }

    public void runSkeleton() {
        try (ServerSocket socket = new ServerSocket(port)) {
            port = socket.getLocalPort();
            System.out.printf("[SKELETON] In ascolto sulla porta %d...\n", port);

            while (true) {
                Socket client = socket.accept();
                System.out.printf("[SKELETON] Ricevuta nuova connessione da %s:%d\n",
                        client.getInetAddress(),
                        client.getPort());

                Thread thread = new LoggingThread(client, this);
                thread.start();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
