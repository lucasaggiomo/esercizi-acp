package dispatcher;

import java.util.StringTokenizer;

import javax.jms.Connection;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.TextMessage;

import dispatcher.magazzino.Acknowledge;
import dispatcher.magazzino.Articolo;
import dispatcher.magazzino.Empty;
import dispatcher.magazzino.MagazzinoGrpc.MagazzinoBlockingStub;
import io.grpc.StatusRuntimeException;

public class DispatcherThread extends Thread {
    private static final String DELIMITER = "-";

    private Connection connection;
    private TextMessage message;
    private MagazzinoBlockingStub magazzinoStub;

    public DispatcherThread(Connection connection, TextMessage message, MagazzinoBlockingStub magazzinoStub) {
        super();
        this.connection = connection;
        this.message = message;
        this.magazzinoStub = magazzinoStub;
    }

    @Override
    public void run() {
        try {

            // interpreta il messaggio
            String text = message.getText();
            System.out.println("[DISPATCHER_MSG_LISTENER] Messaggio ricevuto: " + text);

            StringTokenizer tokenizer = new StringTokenizer(text, DELIMITER);

            Richiesta richiesta = Richiesta.valueOf(tokenizer.nextToken());

            // gestisce la richiesta inviandola con GRPC al server tramite lo stub
            String risposta = "";
            Articolo articolo = null;
            long id = -1;
            switch (richiesta) {
                case Richiesta.DEPOSITA:
                    id = Long.parseLong(tokenizer.nextToken());
                    articolo = Articolo.newBuilder().setId(id).build();

                    try {
                        Acknowledge ack = magazzinoStub.deposita(articolo);
                        risposta = ack.getMessage();
                        System.out.println("[DISPATCHER_THREAD] Deposita: " + risposta);

                    } catch (StatusRuntimeException e) {
                        System.out.println("[DISPATCHER_THREAD] Deposita failed: " + e.getStatus());
                        risposta = new String("Errore: non depositato");
                    }

                    break;

                case Richiesta.PRELEVA:
                    Empty empty = Empty.newBuilder().build();

                    try {

                        articolo = magazzinoStub.preleva(empty);
                        id = articolo.getId();
                        risposta = Long.toString(id);
                        System.out.println("[DISPATCHER_THREAD] Preleva: " + risposta);

                    } catch (StatusRuntimeException e) {
                        System.out.println("[DISPATCHER_THREAD] Preleva failed: " + e.getStatus());
                        risposta = new String("Errore: non prelevato");
                    }

                    break;
            }

            // invia il messaggio al client python sulla coda indicata nel TextMessage
            Destination codaRisposta = message.getJMSReplyTo();
            System.out.println("[DISPATCHER_MSG_LISTENER] JMSReplyTo: " + codaRisposta.toString());

            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

            TextMessage replyMessage = session.createTextMessage(risposta);

            MessageProducer producer = session.createProducer(codaRisposta);
            producer.send(replyMessage);

            System.out.println("[DISPATCHER_THREAD] Inviata risposta al client: " + risposta);

            producer.close();
            session.close();

        } catch (JMSException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

}
