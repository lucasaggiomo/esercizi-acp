package extractor;

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

public class Extractor {

    public static void main(String[] args) {
        Hashtable<String, String> prop = new Hashtable<>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("topic.data", "data");
        prop.put("topic.temp", "temp");
        prop.put("topic.press", "press");

        try {
            // istanzia il Context per jndi
            Context context = new InitialContext(prop);

            // ottiene gli administered object
            ConnectionFactory factory = (ConnectionFactory) context.lookup("TopicConnectionFactory");
            Destination dataDestination = (Destination) context.lookup("data");
            Destination tempDestination = (Destination) context.lookup("temp");
            Destination pressDestination = (Destination) context.lookup("press");

            Connection connection = factory.createConnection();

            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

            MessageConsumer consumer = session.createConsumer(dataDestination);

            MessageListener listener = new ExtractorDataListener(connection, tempDestination, pressDestination);
            consumer.setMessageListener(listener);

            connection.start(); // avvia la connessione per ricevere

            System.out.println("[EXTRACTOR] In ascolto per i messaggi sul topic data...");

            // consumer.close();
            // session.close();
            // connection.close();

        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }

    }
}
