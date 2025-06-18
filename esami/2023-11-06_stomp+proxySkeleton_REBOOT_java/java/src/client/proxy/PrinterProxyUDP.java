package client.proxy;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

import printer.TipoStampa;
import printer.proxy.PrinterProxy;

public class PrinterProxyUDP extends PrinterProxy {

    public PrinterProxyUDP(String host, int port) {
        super(host, port);
    }

    @Override
    public void print(String pathFile, TipoStampa tipo) {
        try (DatagramSocket socket = new DatagramSocket();) {

            System.out.printf("[PROXY] Invio la richiesta di print del file %s con tipo %s\n",
                    pathFile,
                    tipo.toString());

            String request = String.format("%s-%s", pathFile, tipo.toString());
            byte[] buffer = request.getBytes();

            DatagramPacket outputPacket = new DatagramPacket(buffer, buffer.length, InetAddress.getByName(host), port);
            socket.send(outputPacket);

            buffer = new byte[256];
            DatagramPacket inputPacket = new DatagramPacket(buffer, buffer.length);
            socket.receive(inputPacket);

            // attende l'ack
            String response = new String(inputPacket.getData());
            System.out.printf(" [PROXY] Ho ricevuto %s\n", response);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}