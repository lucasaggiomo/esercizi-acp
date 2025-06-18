package server.skeleton.udp;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.StringTokenizer;

import printer.IPrinter;
import printer.TipoStampa;

public class PrinterSkeletonThreadUDP extends Thread {
    private final DatagramSocket socket;
    private final DatagramPacket inputPacket;
    private final IPrinter printer;

    public PrinterSkeletonThreadUDP(
            DatagramSocket socket,
            DatagramPacket inputPacket,
            IPrinter printer) {
        this.socket = socket;
        this.inputPacket = inputPacket;
        this.printer = printer;
    }

    @Override
    public void run() {
        try {
            String text = new String(inputPacket.getData());

            StringTokenizer tokenizer = new StringTokenizer(text, "-");

            String pathFile = tokenizer.nextToken();

            String risposta = null;
            try {
                String giorgio = tokenizer.nextToken().trim();
                TipoStampa tipo = TipoStampa.fromName(giorgio);

                System.out.printf(" [SKELETON-THREAD] Effettuo la stampa del file %s con tipo %s\n",
                        pathFile,
                        tipo.toString());

                printer.print(pathFile, tipo);

                risposta = "ACK";

            } catch (IllegalArgumentException e) {
                System.out.println("    [SKELETON-THREAD] Tipo stampa non riconosciuto");
                risposta = "Tipo stampa non riconosciuto";
            }

            byte[] buffer = risposta.getBytes();
            DatagramPacket outputPacket = new DatagramPacket(buffer, buffer.length, inputPacket.getSocketAddress());
            socket.send(outputPacket);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
