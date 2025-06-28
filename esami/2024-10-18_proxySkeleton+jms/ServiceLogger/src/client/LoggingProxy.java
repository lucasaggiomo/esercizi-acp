package client;

import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;

import logging.ILogging;
import logging.LogType;

public class LoggingProxy implements ILogging {

    private String host;
    private int port;

    public LoggingProxy(String host, int port) {
        this.host = host;
        this.port = port;
    }

    @Override
    public void log(String messaggioLog, LogType tipo) {
        try (
                Socket socket = new Socket(InetAddress.getByName(host), port);
                DataOutputStream outputStream = new DataOutputStream(
                        new BufferedOutputStream(socket.getOutputStream()));) {

            System.out.printf("    [PROXY] Invio il messaggio '%s' di tipo %s (%d)\n",
                    messaggioLog,
                    tipo.toString(),
                    tipo.getIntValue());

            outputStream.writeUTF(messaggioLog);
            outputStream.writeInt(tipo.getIntValue());
            outputStream.flush();

        } catch (IOException e) {
            System.out.println("ERRORE: " + e.toString());
            e.printStackTrace();
        }
    }

}
