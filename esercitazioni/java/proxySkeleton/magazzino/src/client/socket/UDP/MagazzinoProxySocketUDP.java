package client.socket.UDP;

import java.io.IOException;
import java.net.InetAddress;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

import magazzino.Articolo;
import magazzino.Command;
import magazzino.IMagazzino;

public class MagazzinoProxySocketUDP implements IMagazzino {

    private String host;
    private int port;

    public MagazzinoProxySocketUDP(String host, int port) {
        this.host = host;
        this.port = port;
    }

    @Override
    public void deposita(Articolo articolo, int id) {
        try (DatagramSocket socket = new DatagramSocket()) {

            System.out.printf("[PROXY] Invio una richiesta di deposito dell'articolo %s con id %d\n",
                    articolo.name(), id);

            String message = String.format("%s#%s#%d#", Command.DEPOSITA.name(), articolo.name(), id);
            byte[] buffer = message.getBytes();
            DatagramPacket outputPacket = new DatagramPacket(buffer, buffer.length, InetAddress.getByName(host), port);
            socket.send(outputPacket);

            buffer = new byte[256];
            DatagramPacket inputPacket = new DatagramPacket(buffer, buffer.length);
            socket.receive(inputPacket);
            String ack = new String(inputPacket.getData());
            System.out.printf(
                    "[PROXY] Ho ricevuto %s riguardo la richiesta di deposito dell'articolo %s con id %d\n",
                    ack, articolo.name(), id);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public int preleva(Articolo articolo) {
        int id = -1;

        try (DatagramSocket socket = new DatagramSocket()) {

            System.out.printf("[PROXY] Invio una richiesta di prelievo di un articolo %s\n", articolo.name());

            String message = String.format("%s#%s#", Command.PRELEVA.name(), articolo.name());
            byte[] buffer = message.getBytes();
            DatagramPacket outputPacket = new DatagramPacket(buffer, buffer.length, InetAddress.getByName(host), port);
            socket.send(outputPacket);

            buffer = new byte[256];
            DatagramPacket inputPacket = new DatagramPacket(buffer, buffer.length);
            socket.receive(inputPacket);
            id = Integer.valueOf(new String(inputPacket.getData(), 0, inputPacket.getLength()));
            System.out.printf("[PROXY] Ho ricevuto l'id %d riguardo la richiesta di deposito dell'articolo %s\n",
                    id, articolo.name());

        } catch (IOException e) {
            e.printStackTrace();
        }

        return id;
    }

}
