package dispatcher;

import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

import dispatcher.magazzino.MagazzinoGrpc.MagazzinoBlockingStub;

import javax.jms.Connection;

public class DispatcherListener implements MessageListener {
    private Connection connection;
    private MagazzinoBlockingStub magazzinoStub;

    public DispatcherListener(Connection connection, MagazzinoBlockingStub magazzinoStub) {
        super();
        this.connection = connection;
        this.magazzinoStub = magazzinoStub;
    }

    @Override
    public void onMessage(Message message) {

        TextMessage textMessage = (TextMessage) message;

        // crea un thread che gestisce la richiesta, passandogli:
        // - il messaggio per permettere al thread per interpretare la richiesta
        // - lo stub per permettere al thread di delegare la richiesta al server python
        // - la connection, per permettere al thread di mandare la risposta al client python
        Thread thread = new DispatcherThread(connection, textMessage, magazzinoStub);
        thread.start();
    }

}
