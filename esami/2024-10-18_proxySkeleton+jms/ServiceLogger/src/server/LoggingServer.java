package server;

import java.util.Hashtable;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

public class LoggingServer {
    private static int port = 0;

    public static void main(String[] args) {
        Hashtable<String, String> prop = new Hashtable<String, String>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("queue.error", "error");
        prop.put("queue.info", "info");

        try {
            Context context = new InitialContext(prop);

            // ottiene gli administered object
            ConnectionFactory factory = (ConnectionFactory) context.lookup("QueueConnectionFactory");
            Destination errorDest = (Destination) context.lookup("error");
            Destination infoDest = (Destination) context.lookup("info");

            // crea la connessione
            Connection connection = factory.createConnection();

            // crea l'implementazione del server
            LoggingImpl loggingServer = new LoggingImpl(port, connection, errorDest, infoDest);
            loggingServer.runSkeleton();

        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }

    }
}
