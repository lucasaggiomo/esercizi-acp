package loggerListeners.info;

import java.io.PrintStream;

import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.Message;
import javax.jms.MessageListener;

import logging.LogType;

public class InfoFilterListener implements MessageListener {

    private final PrintStream outputStream;

    public InfoFilterListener(PrintStream outputStream) {
        this.outputStream = outputStream;
    }

    @Override
    public void onMessage(Message message) {
        MapMessage mapMessage = (MapMessage) message;
        try {
            String messaggioLog = mapMessage.getString("messaggioLog");
            LogType tipo = LogType.fromIntValue(mapMessage.getInt("tipo"));

            String line = String.format("[%s] %s", tipo.toString(), messaggioLog);

            System.out.printf("[INFO FILTER] Ricevuto il messaggio di log %s\n", line);
            if (tipo != LogType.fromIntValue(1)) {
                System.out.println("        [INFO FILTER] Skipped");
                return;
            }

            outputStream.println(line);

        } catch (JMSException e) {
            e.printStackTrace();
        }
    }
}
