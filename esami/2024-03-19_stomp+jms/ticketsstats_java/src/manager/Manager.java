package manager;

import java.util.Hashtable;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageConsumer;
import javax.jms.Session;
import javax.jms.Connection;

public class Manager {

    public static void main(String args[]) {
        Hashtable<String, String> prop = new Hashtable<>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("topic.requests", "requests");
        prop.put("topic.tickets", "tickets");
        prop.put("topic.stats", "stats");

        // istanzia il context (per contattare il servizio di jndi)
        try {
            Context context = new InitialContext(prop);

            // effettua il lookup degli administered object
            ConnectionFactory factory = (ConnectionFactory) context.lookup("TopicConnectionFactory");

            Destination requests = (Destination) context.lookup("requests");
            Destination tickets = (Destination) context.lookup("tickets");
            Destination stats = (Destination) context.lookup("stats");

            Connection connection = factory.createConnection();
            connection.start();

            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageConsumer consumer = session.createConsumer(requests);

            RequestListener requestListener = new RequestListener(connection, stats, tickets);
            consumer.setMessageListener(requestListener);

            System.out.println("[MANAGER] In attesa di richieste sulla topic...");

        } catch (NamingException e) {
            e.printStackTrace();
        } catch (JMSException e) {
            e.printStackTrace();
        }
    }
}
