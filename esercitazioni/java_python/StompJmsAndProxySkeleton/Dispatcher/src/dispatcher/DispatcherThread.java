package dispatcher;

import java.util.StringTokenizer;

import javax.jms.JMSException;
import javax.jms.Queue;
import javax.jms.QueueConnection;
import javax.jms.QueueSender;
import javax.jms.QueueSession;
import javax.jms.Session;
import javax.jms.TextMessage;

public class DispatcherThread extends Thread {
    private final static String DELIMITER = "-";

    private QueueConnection connection;
    private TextMessage message;

    public DispatcherThread(QueueConnection connection, TextMessage message) {
        this.message = message;
        this.connection = connection;
    }

    @Override
    public void run() {
        String result = eseguiRichiesta();
        mandaRisposta(result);
    }

    private String eseguiRichiesta() {
        String result = "-1";
        try {
            String text = message.getText();

            System.out.println("[THREAD] Ricevuto messaggio: " + text);

            StringTokenizer tokenizer = new StringTokenizer(text, DELIMITER);

            Metodo method = Metodo.valueOf(tokenizer.nextToken());

            switch (method) {
                case PRELEVA:
                    // comunicazione con il server tramite proxy

                    result = "10";

                    break;

                case DEPOSITA:

                    int IDArticolo = Integer.parseInt(tokenizer.nextToken());

                    // comunicazione con il server tramite proxy

                    result = "ACK";

                    break;
            }

        } catch (IllegalArgumentException e) {
            System.out.println("[THREAD] Metodo non supportato");
        } catch (JMSException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        return result;
    }

    private void mandaRisposta(String risposta) {
        try {
            Queue codaRisposta = (Queue) message.getJMSReplyTo();
            QueueSession session = connection.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
            QueueSender sender = session.createSender(codaRisposta);

            TextMessage rispostaMessage = session.createTextMessage(risposta);
            sender.send(rispostaMessage);

        } catch (JMSException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

}
