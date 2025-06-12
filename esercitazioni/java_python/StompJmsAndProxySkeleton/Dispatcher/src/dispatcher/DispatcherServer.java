package dispatcher;

import java.util.Hashtable;

import javax.jms.JMSException;
import javax.jms.Queue;
import javax.jms.QueueConnection;
import javax.jms.QueueConnectionFactory;
import javax.jms.QueueReceiver;
import javax.jms.QueueSession;
import javax.jms.Session;
import javax.naming.InitialContext;
import javax.naming.NamingException;

public class DispatcherServer {
    public static void main(String[] args) {
        Hashtable<String, String> properties = new Hashtable<>();
        properties.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        properties.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        properties.put("queue.richiesta", "richiesta");

        try {
            InitialContext context = new InitialContext(properties);
            Queue codaRichiesta = (Queue) context.lookup("richiesta");
            QueueConnectionFactory factory = (QueueConnectionFactory) context.lookup("QueueConnectionFactory");

            QueueConnection connection = factory.createQueueConnection();
            connection.start();

            QueueSession session = connection.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);

            QueueReceiver receiver = session.createReceiver(codaRichiesta);

            DispatcherListener listener = new DispatcherListener(connection);
            receiver.setMessageListener(listener);

            System.out.println("[DISPATCHER] In attesa di messaggi...");

        } catch (NamingException | JMSException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }
}
