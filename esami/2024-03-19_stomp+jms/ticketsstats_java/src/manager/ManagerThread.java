package manager;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;

import javax.jms.Connection;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.TextMessage;

import requests.Richiesta;

public class ManagerThread extends Thread {

    private final String ARTIST_PATH = "tickets.txt";
    private final MapMessage message;
    private final Connection connection;
    private final Destination statsDestination;
    private final Destination ticketsDestination;

    public ManagerThread(
            MapMessage message,
            Connection connection,
            Destination statsDestination,
            Destination ticketsDestination) {
        this.message = message;
        this.connection = connection;
        this.statsDestination = statsDestination;
        this.ticketsDestination = ticketsDestination;
    }

    @Override
    public void run() {
        try {
            Richiesta tipoRichiesta = null;
            try {
                tipoRichiesta = Richiesta.valueOf(message.getString("type"));
            } catch (IllegalArgumentException e) {
                System.out.println("[CLIENT] Richiesta non riconosciuta");
                return;
            }

            String value = message.getString("value");

            System.out.printf("[MANAGER] Ricevuto una richiesta con type = %s e value = %s\n", tipoRichiesta, value);

            Destination destination = null;

            switch (tipoRichiesta) {
                case BUY:
                    destination = ticketsDestination;
                    writeArtistToFile(value);
                    break;
                case STATS:
                    destination = statsDestination;
                    break;
            }
            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageProducer producer = session.createProducer(destination);

            TextMessage textMessage = session.createTextMessage();
            textMessage.setText(value);
            System.out.println(
                    "        [MANAGER] Invio sulla coda " + (tipoRichiesta == Richiesta.STATS ? "stats" : "tickets")
                            + " il messaggio " + textMessage.getText());
            producer.send(textMessage);

        } catch (JMSException e) {
            e.printStackTrace();
        }
    }

    private void writeArtistToFile(String artist) {
        System.out.println("        [MANAGER] Scrivo sul file " + ARTIST_PATH + " l'artista " + artist);
        try (PrintStream file = new PrintStream(new FileOutputStream(ARTIST_PATH, true))) {

            file.println(artist);

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

    }

}
