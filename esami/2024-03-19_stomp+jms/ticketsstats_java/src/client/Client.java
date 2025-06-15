package client;

import java.util.Hashtable;
import java.util.Random;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.Connection;

import requests.Richiesta;

public class Client {
    private static final int NUM_RICHIESTE = 20;
    private static final String[] Artisti = new String[] { "Jovanotti", "Ligabue", "Negramaro" };
    private static final String STATS_STRING = "Sold";
    private static final Random rand = new Random();

    public static void main(String args[]) {
        Richiesta tipoRichiesta = null;
        try {
            tipoRichiesta = Richiesta.valueOf(args[0].toUpperCase());
        } catch (IndexOutOfBoundsException e) {
            System.out.println("Inserisci il tipo di richiesta");
            System.exit(1);
            return;
        } catch (IllegalArgumentException e) {
            System.out.println("La richiesta inserita non è stata riconosciuta");
            System.exit(1);
            return;
        }

        Hashtable<String, String> prop = new Hashtable<>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("topic.requests", "requests");

        // istanzia il context (per contattare il servizio di jndi)
        try {
            Context context = new InitialContext(prop);

            // effettua il lookup degli administered object
            ConnectionFactory factory = (ConnectionFactory) context.lookup("TopicConnectionFactory");
            Destination requests = (Destination) context.lookup("requests");

            Connection connection = factory.createConnection();
            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

            MessageProducer producer = session.createProducer(requests);

            for (int i = 0; i < NUM_RICHIESTE; i++) {
                MapMessage message = session.createMapMessage();
                message.setString("type", tipoRichiesta.toString());

                String valore = null;
                switch (tipoRichiesta) {
                    case BUY:
                        valore = Artisti[rand.nextInt(Artisti.length)];
                        break;
                    case STATS:
                        valore = STATS_STRING;
                        break;
                }
                message.setString("value", valore);

                System.out.printf("[CLIENT] Invio sulla topic 'requests' il messaggio con type %s e value %s\n",
                        tipoRichiesta, valore);
                producer.send(message);

                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            producer.close();
            session.close();
            connection.close();

        } catch (NamingException e) {
            e.printStackTrace();
        } catch (JMSException e) {
            e.printStackTrace();
        }
    }
}
