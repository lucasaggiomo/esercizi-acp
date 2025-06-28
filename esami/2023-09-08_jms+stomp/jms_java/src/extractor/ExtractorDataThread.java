package extractor;

import javax.jms.Connection;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.TextMessage;

import richieste.TipoRichiesta;

public class ExtractorDataThread extends Thread {

    private final MapMessage mapMessage;
    private final Connection connection;
    private final Destination tempDestination;
    private final Destination pressDestination;

    public ExtractorDataThread(
            MapMessage mapMessage,
            Connection connection,
            Destination tempDestination,
            Destination pressDestination) {
        this.mapMessage = mapMessage;
        this.connection = connection;
        this.tempDestination = tempDestination;
        this.pressDestination = pressDestination;
    }

    @Override
    public void run() {

        try {
            TipoRichiesta type = null;
            try {
                type = TipoRichiesta.valueOf(mapMessage.getString("type"));
            } catch (IllegalArgumentException e) {
                System.out.println("Tipo di richiesta non riconosciuto");
                return;
            }
            int value = mapMessage.getInt("value");

            System.out.printf("[EXTRACTOR LISTENER] Ho ricevuto la richiesta %s con valore %d\n", type, value);

            // invia un TextMessage alla destinazione opportuna
            Destination destination = null;
            switch (type) {
                case PRESSURE:
                    destination = pressDestination;
                    break;
                case TEMPERATURE:
                    destination = tempDestination;
                    break;
            }

            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageProducer producer = session.createProducer(destination);

            TextMessage textMessage = session.createTextMessage();
            textMessage.setText(Integer.toString(value));

            producer.send(textMessage);

        } catch (JMSException e) {
            e.printStackTrace();
        }

    }

}
