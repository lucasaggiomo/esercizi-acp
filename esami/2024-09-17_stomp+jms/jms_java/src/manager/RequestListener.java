package manager;

import javax.jms.Connection;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MapMessage;
import javax.jms.Message;
import javax.jms.MessageListener;

import richieste.TipoRichiesta;

public class RequestListener implements MessageListener {

    private final Connection connection;
    private final Destination compraDest;
    private final Destination vendiDest;

    public RequestListener(Connection connection, Destination compraDest, Destination vendiDest) {
        this.connection = connection;
        this.compraDest = compraDest;
        this.vendiDest = vendiDest;
    }

    @Override
    public void onMessage(Message message) {
        MapMessage mapMessage = (MapMessage) message;

        try {
            TipoRichiesta tipo = null;
            try {

                tipo = TipoRichiesta.valueOf(mapMessage.getString("tipo"));

            } catch (IllegalArgumentException e) {
                System.out.println("[REQUEST_LISTENER] Tipo non riconosciuto");
                return;
            }

            Destination dest = null;
            switch (tipo) {
                case COMPRA:
                    dest = this.compraDest;
                    break;
                case VENDI:
                    dest = this.vendiDest;
                    break;
            }

            String valore = mapMessage.getString("valore");

            System.out.printf("[REQUEST_LISTENER] Ho ricevuto una richiesta con tipo %s e valore %s\n", tipo.toString(),
                    valore);

            Thread thread = new RequestSenderThread(connection, dest, valore);
            thread.start();

        } catch (JMSException e) {
            e.printStackTrace();
        }

    }
}
