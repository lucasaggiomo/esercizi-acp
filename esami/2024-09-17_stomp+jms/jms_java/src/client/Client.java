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

    private static final int NUM_RICHIESTE = 20;

    private static final Random rand = new Random();

    // targhe e utenti di esempio
    private static final String[] Targhe_veicoli = new String[] { "AA000BB", "CC111DD", "EE222FF", "GG333HH",
            "II444HH" };
    private static final String[] IDClienti = new String[] { "giovanni", "giggino", "giorgiovanni", "gianluca",
            "gianmarco" };

    public static void main(String[] args) {

        TipoRichiesta tipo = null;
        if (args.length == 0) {
            System.out.println("Inserisci il tipo delle richieste");
            System.exit(1);
        }
        try {
            tipo = TipoRichiesta.valueOf(args[0].toUpperCase());
        } catch (IllegalArgumentException e) {
            System.out.println("Tipo di richiesta non riconosciuto");
            System.exit(1);
        }

        Hashtable<String, String> prop = new Hashtable<>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("topic.request", "request");

        try {
            // context per il servizio jndi
            Context context = new InitialContext(prop);

            // risolve gli administered object
            ConnectionFactory factory = (ConnectionFactory) context.lookup("TopicConnectionFactory");
            Destination requestDest = (Destination) context.lookup("request");

            Connection connection = factory.createConnection();
            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageProducer producer = session.createProducer(requestDest);

            for (int i = 0; i < NUM_RICHIESTE; i++) {

                String valore = null;

                switch (tipo) {
                    case VENDI:
                        String targa = Targhe_veicoli[rand.nextInt(Targhe_veicoli.length)];
                        int quotazione = 1000 + rand.nextInt(1500);
                        valore = String.format("%s-%d", targa, quotazione);
                        break;
                    case COMPRA:
                        String idCliente = IDClienti[rand.nextInt(IDClienti.length)];
                        int budget = 2000 + rand.nextInt(1000);
                        valore = String.format("%s-%d", idCliente, budget);
                        break;
                }

                System.out.printf("[CLIENT] Invio una richiesta con tipo %s e valore %s\n", tipo, valore);

                MapMessage message = session.createMapMessage();
                message.setString("tipo", tipo.toString());
                message.setString("valore", valore);

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

        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }
    }
}
