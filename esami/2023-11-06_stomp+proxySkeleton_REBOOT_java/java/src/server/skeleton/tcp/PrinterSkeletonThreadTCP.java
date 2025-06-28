package server.skeleton.tcp;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

import printer.IPrinter;
import printer.TipoStampa;

public class PrinterSkeletonThreadTCP extends Thread {

    private final Socket clientSocket;
    private final IPrinter printer;

    public PrinterSkeletonThreadTCP(Socket clientSocket, IPrinter printer) {
        this.clientSocket = clientSocket;
        this.printer = printer;
    }

    @Override
    public void run() {
        try (
                DataInputStream inputStream = new DataInputStream(
                        new BufferedInputStream(clientSocket.getInputStream()));
                DataOutputStream outputStream = new DataOutputStream(
                        new BufferedOutputStream(clientSocket.getOutputStream()));) {

            String risposta = null;

            String pathFile = inputStream.readUTF();

            try {
                TipoStampa tipo = TipoStampa.fromName(inputStream.readUTF());

                System.out.printf(" [SKELETON-THREAD] Effettuo la stampa del file %s con tipo %s\n",
                        pathFile,
                        tipo.toString());

                printer.print(pathFile, tipo);

                risposta = "ACK";

            } catch (IllegalArgumentException e) {
                System.out.println("    [SKELETON-THREAD] Tipo stampa non riconosciuto");
                risposta = "Tipo stampa non riconosciuto";
            }

            outputStream.writeUTF(risposta);
            outputStream.flush();

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                clientSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

}
