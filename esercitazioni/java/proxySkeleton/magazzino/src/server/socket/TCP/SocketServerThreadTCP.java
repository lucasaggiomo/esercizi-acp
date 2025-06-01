package server.socket.TCP;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

import magazzino.Articolo;
import magazzino.Command;
import magazzino.IMagazzino;

public class SocketServerThreadTCP extends Thread {

    private final Socket socket;
    private final IMagazzino magazzinoService;

    public SocketServerThreadTCP(Socket socket, IMagazzino magazzinoService) {
        this.socket = socket;
        this.magazzinoService = magazzinoService;
    }

    @Override
    public void run() {
        try (
                DataInputStream inputStream = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
                DataOutputStream outputStream = new DataOutputStream(
                        new BufferedOutputStream(socket.getOutputStream()));) {

            // assume comandi e articoli corretti
            Command command = Command.valueOf(inputStream.readUTF());
            Articolo articolo = null;
            int id = -1;

            switch (command) {
                case Command.DEPOSITA:
                    articolo = Articolo.valueOf(inputStream.readUTF());
                    id = inputStream.readInt();

                    System.out.printf("[SOCKET_SERVER_THREAD - %s] Provo a depositare l'articolo %s con id %d\n",
                            this.getName(), articolo.name(), id);

                    magazzinoService.deposita(articolo, id);

                    System.out.printf("[SOCKET_SERVER_THREAD - %s] Mando l'ACK\n", this.getName());
                    outputStream.writeUTF("ACK");
                    outputStream.flush();

                    break;

                case Command.PRELEVA:
                    articolo = Articolo.valueOf(inputStream.readUTF());
                    System.out.printf("[SOCKET_SERVER_THREAD - %s] Provo a prelevare un articolo %s\n",
                            this.getName(), articolo.name());

                    id = magazzinoService.preleva(articolo);

                    System.out.printf("[SOCKET_SERVER_THREAD - %s] Mando l'id %d\n", this.getName(), id);
                    outputStream.writeInt(id);
                    outputStream.flush();

                    break;

            }

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            silentlyCloseSocket();
        }

    }

    public void silentlyCloseSocket() {
        try {
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
