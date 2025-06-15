package loggerListeners.info;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Hashtable;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageConsumer;
import javax.jms.MessageListener;
import javax.jms.Session;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

public class InfoFilter {
    public static void main(String[] args) {
        Hashtable<String, String> prop = new Hashtable<String, String>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("queue.info", "info");

        try {
            Context context = new InitialContext(prop);

            // ottiene gli administered object
            ConnectionFactory factory = (ConnectionFactory) context.lookup("QueueConnectionFactory");
            Destination destination = (Destination) context.lookup("info");

            // crea la connessione
            Connection connection = factory.createConnection();
            connection.start(); // avvia la connessione per abilitare la ricezione

            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

            PrintStream infoFileStream = new PrintStream(new FileOutputStream("info.txt", true));

            MessageListener listener = new InfoFilterListener(infoFileStream);

            MessageConsumer consumer = session.createConsumer(destination);

            consumer.setMessageListener(listener);

            System.out.println("[INFO FILTER] Sono in ascolto sulla coda info...");

            // infoFileStream.close();
            // session.close();
            // connection.close();

        } catch (NamingException | JMSException | FileNotFoundException e) {
            e.printStackTrace();
        }

    }
}
