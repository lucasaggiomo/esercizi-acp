package client.socket.TCP;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;

import magazzino.Articolo;
import magazzino.Command;
import magazzino.IMagazzino;

public class MagazzinoProxySocketTCP implements IMagazzino {

    private String host;
    private int port;

    public MagazzinoProxySocketTCP(String host, int port) {
        this.host = host;
        this.port = port;
    }

    @Override
    public void deposita(Articolo articolo, int id) {
        try (
                Socket socket = new Socket(InetAddress.getByName(host), port);
                DataInputStream inputStream = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
                DataOutputStream outputStream = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));
            ) {

            System.out.printf("\t[PROXY] Invio una richiesta di deposito dell'articolo %s con id %d\n", articolo.name(), id);

            outputStream.writeUTF(Command.DEPOSITA.name());
            outputStream.writeUTF(articolo.name());
            outputStream.writeInt(id);
            outputStream.flush();

            String ack = inputStream.readUTF();
            System.out.printf("\t[PROXY] Ho ricevuto %s riguardo la richiesta di deposito dell'articolo %s con id %d\n", ack, articolo.name(), id);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public int preleva(Articolo articolo) {
        int id = -1;

        try (
                Socket socket = new Socket(InetAddress.getByName(host), port);
                DataInputStream inputStream = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
                DataOutputStream outputStream = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));
            ) {

            System.out.printf("\t[PROXY] Invio una richiesta di prelievo di un articolo %s\n", articolo.name());

            outputStream.writeUTF(Command.PRELEVA.name());
            outputStream.writeUTF(articolo.name());
            outputStream.flush();

            id = inputStream.readInt();
            System.out.printf("\t[PROXY] Ho ricevuto l'id %d riguardo la richiesta di deposito dell'articolo %s\n", id, articolo.name());

        } catch (IOException e) {
            e.printStackTrace();
        }

        return id;
    }

}
