package manager;

import javax.jms.Connection;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.TextMessage;

public class RequestSenderThread extends Thread {

    private final Connection connection;
    private final Destination destination;
    private final String valore;

    public RequestSenderThread(Connection connection, Destination dest, String valore) {
        this.connection = connection;
        this.destination = dest;
        this.valore = valore;
    }

    @Override
    public void run() {

        try {

            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageProducer producer = session.createProducer(destination);

            TextMessage message = session.createTextMessage(this.valore);

            System.out.printf("[REQUEST_SENDER_THREAD] Invio la richiesta con testo %s sulla coda opportuna\n",
                    this.valore);

            producer.send(message);

            producer.close();
            session.close();

        } catch (JMSException e) {
            e.printStackTrace();
        }
    }

}
