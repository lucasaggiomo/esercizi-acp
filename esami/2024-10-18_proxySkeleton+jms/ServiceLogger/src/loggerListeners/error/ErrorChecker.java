package loggerListeners.error;

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

public class ErrorChecker {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Inserisci una stringa tra 'fatal' e 'exception'");
            System.exit(1);
            return;
        }

        String message = args[0];
        if (!message.equals("fatal") && !message.equals("exception")) {
            System.out.println("Inserisci una stringa tra 'fatal' e 'exception'");
            System.exit(1);
            return;
        }

        Hashtable<String, String> prop = new Hashtable<String, String>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("queue.error", "error");

        try {
            Context context = new InitialContext(prop);

            // ottiene gli administered object
            ConnectionFactory factory = (ConnectionFactory) context.lookup("QueueConnectionFactory");
            Destination destination = (Destination) context.lookup("error");

            // crea la connessione
            Connection connection = factory.createConnection();
            connection.start(); // avvia la connessione per abilitare la ricezione

            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

            PrintStream errorFileStream = new PrintStream(new FileOutputStream("error.txt", true));

            MessageListener listener = new ErrorCheckerListener(message, errorFileStream);

            MessageConsumer consumer = session.createConsumer(destination);

            consumer.setMessageListener(listener);

            System.out.println("[ERROR CHECKER] Sono in ascolto sulla coda error...");

            // errorFileStream.close();
            // session.close();
            // connection.close();

        } catch (NamingException | JMSException | FileNotFoundException e) {
            e.printStackTrace();
        }

    }
}
