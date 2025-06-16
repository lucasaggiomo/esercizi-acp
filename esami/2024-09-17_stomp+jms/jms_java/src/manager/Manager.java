package manager;

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

public class Manager {

    public static void main(String[] args) {

        Hashtable<String, String> prop = new Hashtable<>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("topic.request", "request");
        prop.put("topic.compra", "compra");
        prop.put("topic.vendi", "vendi");

        try {
            // context per il servizio jndi
            Context context = new InitialContext(prop);

            // risolve gli administered object
            ConnectionFactory factory = (ConnectionFactory) context.lookup("TopicConnectionFactory");
            Destination requestDest = (Destination) context.lookup("request");
            Destination compraDest = (Destination) context.lookup("compra");
            Destination vendiDest = (Destination) context.lookup("vendi");

            Connection connection = factory.createConnection();
            connection.start(); // avvia la connessione per abilitare la ricezione

            MessageListener requestListener = new RequestListener(connection, compraDest, vendiDest);

            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageConsumer consumer = session.createConsumer(requestDest);
            consumer.setMessageListener(requestListener);

            System.out.println("[MANAGER] In ascolto sul topic request...");

        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }
    }
}
