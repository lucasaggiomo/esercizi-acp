package client;

import java.util.Hashtable;

import java.util.Random;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

import richieste.TipoRichiesta;

public class Client {

    private static int NUM_RICHIESTE = 20;

    private static final Random rand = new Random();

    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Inserisci il tipo di richiesta");
            return;
        }

        TipoRichiesta type;
        try {
            type = TipoRichiesta.valueOf(args[0].toUpperCase());
        } catch (IllegalArgumentException e) {
            System.out.println("Tipo di richiesta non riconosciuto: " + args[0]);
            return;
        }

        Hashtable<String, String> prop = new Hashtable<>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("topic.data", "data");

        try {
            // istanzia il Context per jndi
            Context context = new InitialContext(prop);

            // ottiene gli administered object
            ConnectionFactory factory = (ConnectionFactory) context.lookup("TopicConnectionFactory");
            Destination dataDestination = (Destination) context.lookup("data");

            Connection connection = factory.createConnection();
            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

            MessageProducer producer = session.createProducer(dataDestination);

            for (int i = 0; i < NUM_RICHIESTE; i++) {
                int value = -1;
                switch (type) {
                    case PRESSURE:
                        value = 1000 + rand.nextInt(51);
                        break;
                    case TEMPERATURE:
                        value = rand.nextInt(101);
                        break;
                }

                MapMessage message = session.createMapMessage();
                message.setString("type", type.toString());
                message.setInt("value", value);

                System.out.printf("[CLIENT] Invio messaggio {'type': '%s', 'value': %d} sul topic 'data'\n",
                        type,
                        value);

                producer.send(message);

                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            // effettua il clean-up delle risorse
            producer.close();
            session.close();
            connection.close();

        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }

    }
}
