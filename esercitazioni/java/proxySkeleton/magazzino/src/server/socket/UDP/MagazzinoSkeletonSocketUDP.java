package server.socket.UDP;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

import magazzino.IMagazzino;
import server.MagazzinoSkeleton;

public class MagazzinoSkeletonSocketUDP extends MagazzinoSkeleton {
    private int port;

    public MagazzinoSkeletonSocketUDP(IMagazzino magazzino, int port) {
        super(magazzino);
        this.port = port;
    }

    @Override
    public void runSkeleton() {
        try (DatagramSocket socket = new DatagramSocket(port)) {
            port = socket.getLocalPort();
            System.out.printf("[SKELETON] Waiting on port %d...\n", port);

            while (true) {
                byte[] buffer = new byte[256];
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                socket.receive(packet);
                String data = new String(packet.getData());

                System.out.printf("[SKELETON] Received %s from %s:%s\n",
                        data,
                        packet.getAddress(),
                        packet.getPort());

                Thread thread = new SocketThreadUDP(socket, packet, this);
                thread.start();
            }

        } catch (IOException e) {
            System.out.println("[SKELETON] Errore: " + e.getMessage());
        }
    }

}
