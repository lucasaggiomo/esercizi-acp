package loggerListeners.error;

import java.io.PrintStream;

import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.Message;
import javax.jms.MessageListener;

import logging.LogType;

public class ErrorCheckerListener implements MessageListener {

    private final String messaggioLog;
    private final PrintStream outputStream;

    public ErrorCheckerListener(String messaggioLog, PrintStream outputStream) {
        this.messaggioLog = messaggioLog;
        this.outputStream = outputStream;
    }

    @Override
    public void onMessage(Message message) {
        MapMessage mapMessage = (MapMessage) message;
        try {
            String realMessageLog = mapMessage.getString("messaggioLog");
            LogType tipo = LogType.fromIntValue(mapMessage.getInt("tipo"));

            String line = String.format("[%s] %s", tipo.toString(), messaggioLog);

            System.out.printf("[ERROR CHECKER] Ricevuto il messaggio di log %s\n", line);
            if (!realMessageLog.equals(messaggioLog)) {
                System.out.println("        [ERROR CHECKER] Skipped");
                return;
            }

            outputStream.println(line);

        } catch (JMSException e) {
            e.printStackTrace();
        }
    }

}
