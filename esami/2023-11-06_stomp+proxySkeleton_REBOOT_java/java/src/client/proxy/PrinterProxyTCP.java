package client.proxy;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;

import printer.TipoStampa;
import printer.proxy.PrinterProxy;

public class PrinterProxyTCP extends PrinterProxy {

    public PrinterProxyTCP(String host, int port) {
        super(host, port);
    }

    @Override
    public void print(String pathFile, TipoStampa tipo) {
        try (
                Socket socket = new Socket(InetAddress.getByName(host), port);
                DataInputStream inputStream = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
                DataOutputStream outputStream = new DataOutputStream(
                        new BufferedOutputStream(socket.getOutputStream()));) {

            System.out.printf("[PROXY] Invio la richiesta di print del file %s con tipo %s\n",
                    pathFile,
                    tipo.toString());

            outputStream.writeUTF(pathFile);
            outputStream.writeUTF(tipo.toString());

            outputStream.flush();

            // attende l'ack
            String response = inputStream.readUTF();
            System.out.printf(" [PROXY] Ho ricevuto %s\n", response);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
