package server.socket.UDP;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.StringTokenizer;

import magazzino.Articolo;
import magazzino.Command;
import magazzino.IMagazzino;

public class SocketThreadUDP extends Thread {
    private final static String DELIIMITERS = "#";

    private final DatagramPacket inputPacket;
    private final DatagramSocket socket;
    private final IMagazzino magazzinoService;

    public SocketThreadUDP(DatagramSocket socket, DatagramPacket inputPacket, IMagazzino magazzinoService) {
        super();
        this.socket = socket;
        this.inputPacket = inputPacket;
        this.magazzinoService = magazzinoService;
    }

    @Override
    public void run() {
        String data = new String(inputPacket.getData());

        StringTokenizer tokenizer = new StringTokenizer(data, DELIIMITERS);
        Command command = Command.valueOf(tokenizer.nextToken());
        Articolo articolo = null;
        int id = -1;

        try {
            DatagramPacket outputPacket = null;
            byte[] buffer = null;

            switch (command) {
                case Command.DEPOSITA:
                    articolo = Articolo.valueOf(tokenizer.nextToken());
                    id = Integer.valueOf(tokenizer.nextToken());
                    magazzinoService.deposita(articolo, id);

                    buffer = "ACK".getBytes();
                    break;

                case Command.PRELEVA:
                    articolo = Articolo.valueOf(tokenizer.nextToken());
                    id = magazzinoService.preleva(articolo);

                    buffer = Integer.toString(id).getBytes();
                    break;

            }

            outputPacket = new DatagramPacket(buffer, buffer.length, inputPacket.getAddress(), inputPacket.getPort());
            socket.send(outputPacket);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
