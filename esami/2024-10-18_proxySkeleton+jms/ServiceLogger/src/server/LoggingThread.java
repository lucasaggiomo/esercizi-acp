package server;

import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;

import logging.ILogging;
import logging.LogType;

public class LoggingThread extends Thread {

    private final Socket socket;
    private final ILogging loggingService;

    public LoggingThread(Socket socket, ILogging loggingService) {
        super();
        this.socket = socket;
        this.loggingService = loggingService;
    }

    @Override
    public void run() {
        try (DataInputStream inputStream = new DataInputStream(new BufferedInputStream(socket.getInputStream()))) {

            // legge gli input della richiesta di log
            String messaggioLog = inputStream.readUTF();
            LogType tipo = LogType.fromIntValue(inputStream.readInt());

            System.out.printf(" [SKELETON] Ho ricevuto una richiesta di log con messaggio '%s' e tipo %s (%d)\n",
                    messaggioLog,
                    tipo.toString(),
                    tipo.getIntValue());

            loggingService.log(messaggioLog, tipo);

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                socket.close();
            } catch (IOException e) {
                System.out.println("[THREAD] Errore nella chiusura della socket!");
                e.printStackTrace();
            }
        }
    }

}
