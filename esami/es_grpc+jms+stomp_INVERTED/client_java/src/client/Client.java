package client;

import java.util.Hashtable;
import java.util.Random;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageConsumer;
import javax.jms.MessageListener;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.TextMessage;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

public class Client {
    private static final int NUM_RICHIESTE = 10;

    private static final String DELIMITER = "-";
    private static final Random random = new Random();

    public static void main(String[] args) {
        Hashtable<String, String> prop = new Hashtable<>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("queue.richiesta", "richiesta");
        prop.put("queue.risposta", "risposta");

        try {
            // context per jndi
            Context context = new InitialContext(prop);

            // administered objects
            ConnectionFactory factory = (ConnectionFactory) context.lookup("QueueConnectionFactory");
            Destination richiestaDest = (Destination) context.lookup("richiesta");
            Destination rispostaDest = (Destination) context.lookup("risposta");

            // il necessario per comunicare
            Connection connection = factory.createConnection();
            connection.start(); // avvia la connessione per abilitare la ricezione

            // crea due sessioni diverse per la ricezione e l'invio (Session non è
            // thread-safe, potrebbe causare race condition )
            Session richiestaSession = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            Session rispostaSession = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

            MessageProducer richiestaProducer = richiestaSession.createProducer(richiestaDest);
            MessageConsumer rispostaConsumer = rispostaSession.createConsumer(rispostaDest);
            MessageListener rispostaListener = new RispostaListener();
            rispostaConsumer.setMessageListener(rispostaListener);

            for (int i = 0; i < NUM_RICHIESTE; i++) {
                TipoRichiesta tipo = null;
                String messaggio = "";
                if (i % 2 == 0) {
                    tipo = TipoRichiesta.DEPOSITA;
                    int id_articolo = random.nextInt(100) + 1;
                    messaggio = String.format("%s%s%d", tipo.toString(), DELIMITER, id_articolo);
                } else {
                    tipo = TipoRichiesta.PRELEVA;
                    messaggio = tipo.toString();
                }

                System.out.printf("[CLIENT] Invio il messaggio %s\n", messaggio);

                TextMessage message = rispostaSession.createTextMessage(messaggio);
                message.setJMSReplyTo(rispostaDest);
                richiestaProducer.send(message);

                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }
    }
}
