package server.skeleton.udp;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

import printer.IPrinter;
import printer.skeleton.PrinterSkeleton;

public class PrinterSkeletonUDP extends PrinterSkeleton {
    public PrinterSkeletonUDP(IPrinter printer) {
        super(printer);
    }

    public PrinterSkeletonUDP(int port, IPrinter printer) {
        super(port, printer);
    }

    @Override
    public void runSkeleton() {
        try (DatagramSocket socket = new DatagramSocket(port)) {
            this.port = socket.getLocalPort();

            System.out.printf("[SKELETON] In ascolto sulla porta %d...\n", port);

            while (true) {
                byte[] buffer = new byte[256];
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                socket.receive(packet);
                String data = new String(packet.getData());

                System.out.printf("[SKELETON] Ricevuto pacchetto %s da %s:%s\n",
                        data,
                        packet.getAddress(),
                        packet.getPort());

                Thread thread = new PrinterSkeletonThreadUDP(socket, packet, this);
                thread.start();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
