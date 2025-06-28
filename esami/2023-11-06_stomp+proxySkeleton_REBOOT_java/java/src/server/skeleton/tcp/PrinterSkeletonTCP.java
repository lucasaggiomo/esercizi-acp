package server.skeleton.tcp;

import printer.IPrinter;
import printer.skeleton.PrinterSkeleton;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class PrinterSkeletonTCP extends PrinterSkeleton {

    public PrinterSkeletonTCP(IPrinter printer) {
        super(printer);
    }

    public PrinterSkeletonTCP(int port, IPrinter printer) {
        super(port, printer);
    }

    @Override
    public void runSkeleton() {
        try (ServerSocket socket = new ServerSocket(port)) {
            this.port = socket.getLocalPort();

            System.out.printf("[SKELETON] In ascolto sulla porta %d...\n", port);

            while (true) {
                Socket client = socket.accept();

                System.out.printf("[SKELETON] Connesso con %s:%s\n",
                        client.getInetAddress(),
                        client.getPort());

                Thread thread = new PrinterSkeletonThreadTCP(client, this);
                thread.start();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
