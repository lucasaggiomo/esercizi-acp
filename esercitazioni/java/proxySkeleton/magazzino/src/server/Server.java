package server;

import magazzino.IMagazzino;
import server.socket.TCP.MagazzinoSkeletonSocketTCP;
import server.socket.UDP.MagazzinoSkeletonSocketUDP;

public class Server {
    private final static int PORT = 0;

    public static void main(String[] args) {
        int capacity;
        try {
            capacity = Integer.parseInt(args[0]);
        } catch (Exception e) {
            System.out.println("Inserisci la capacità del magazzino");
            System.exit(-1);
            return;
        }

        IMagazzino magazzino = new MagazzinoImpl(capacity);
        MagazzinoSkeleton skeleton = new MagazzinoSkeletonSocketTCP(magazzino, PORT);
        skeleton.runSkeleton();
    }
}
