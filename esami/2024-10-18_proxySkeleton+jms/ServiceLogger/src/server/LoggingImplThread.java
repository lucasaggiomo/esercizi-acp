package server;

import javax.jms.Connection;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.MessageProducer;
import javax.jms.Session;

import logging.LogType;

public class LoggingImplThread extends Thread {

    private final String messaggioLog;
    private final LogType tipo;
    private final Connection connection;
    private final Destination destination;

    public LoggingImplThread(String messaggioLog, LogType tipo, Connection connection, Destination destination) {
        this.messaggioLog = messaggioLog;
        this.tipo = tipo;
        this.connection = connection;
        this.destination = destination;
    }

    @Override
    public void run() {

        // Session e MessageProducer non implementano AutoCloseable, quindi il
        // try-with-resources non è utilizzabile
        Session session = null;
        MessageProducer producer = null;
        try {
            session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            producer = session.createProducer(destination);

            MapMessage message = session.createMapMessage();
            message.setString("messaggioLog", messaggioLog);
            message.setInt("tipo", tipo.getIntValue());

            System.out.println("                [LOGGINGIMPLTHREAD] Invio del MapMessage...");
            producer.send(message);

        } catch (JMSException e) {
            e.printStackTrace();
        } finally {
            closeQuitely(session, producer);
        }

    }

    private void closeQuitely(Session session, MessageProducer producer) {
        try {
            if (producer != null)
                producer.close();
            if (session != null)
                session.close();
        } catch (JMSException e) {
            e.printStackTrace();
        }
    }

}
