package server;

import java.util.StringTokenizer;

import javax.jms.Connection;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.TextMessage;

import coda.ICoda;
import coda.exceptions.CodaIsEmptyException;
import printer.TipoStampa;

public class PrinterServerConsumatoreThread extends Thread {

    private final ICoda<String> coda;

    private final Connection connection;
    private final Destination destBW;
    private final Destination destCOLOR;

    public PrinterServerConsumatoreThread(
            ICoda<String> coda,
            Connection connection,
            Destination destBW,
            Destination destCOLOR) {
        this.coda = coda;
        this.connection = connection;
        this.destBW = destBW;
        this.destCOLOR = destCOLOR;
    }

    @Override
    public void run() {
        while (true) {
            System.out.println("    [CONSUMATORE] Consumo dalla coda");
            String item = null;

            try {
                item = coda.pop();
            } catch (CodaIsEmptyException e) {
                e.printStackTrace();
                return;
            }

            System.out.printf(" [CONSUMATORE] OK, ho consumato %s\n", item);

            StringTokenizer tokenizer = new StringTokenizer(item, "-");

            String pathFile = tokenizer.nextToken();
            TipoStampa tipo = null;

            Destination dest = null;
            String destName = null; // solo per stampare a video

            try {

                tipo = TipoStampa.fromName(tokenizer.nextToken());
                if (tipo == TipoStampa.COLOR) {
                    dest = destCOLOR;
                    destName = "queue.color";
                } else {
                    dest = destBW;
                    destName = "queue.bw";
                }

            } catch (IllegalArgumentException e) {
                System.out.println("    [CONSUMATORE] Tipo di stampa non riconosciuto");
                return;
            }

            try {
                Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
                MessageProducer producer = session.createProducer(dest);
                TextMessage message = session.createTextMessage();
                message.setText(item);

                System.out.printf("     [CONSUMATORE] Mando sulla coda '%s' il TextMessage '%s'\n", destName, item);
                producer.send(message);

            } catch (JMSException e) {
                e.printStackTrace();
            }

        }
    }
}
