package server.socket.TCP;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

import magazzino.IMagazzino;
import server.MagazzinoSkeleton;

public class MagazzinoSkeletonSocketTCP extends MagazzinoSkeleton {
    private int port;

    public MagazzinoSkeletonSocketTCP(IMagazzino magazzino, int port) {
        super(magazzino);
        this.port = port;
    }

    @Override
    public void runSkeleton() {
        try (ServerSocket socket = new ServerSocket(port)) {
            port = socket.getLocalPort();
            System.out.printf("\t[SKELETON] Waiting on port %d...\n", port);

            while (true) {
                Socket connectionSocket = socket.accept();

                System.out.printf("\t[SKELETON] Connected with %s:%s\n",
                        connectionSocket.getInetAddress(),
                        connectionSocket.getPort());

                Thread thread = new SocketServerThreadTCP(connectionSocket, this);
                thread.start();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
