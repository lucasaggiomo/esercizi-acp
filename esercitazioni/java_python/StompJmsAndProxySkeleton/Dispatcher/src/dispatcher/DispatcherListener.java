package dispatcher;

import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.QueueConnection;
import javax.jms.TextMessage;

public class DispatcherListener implements MessageListener {

    private QueueConnection connection;

    public DispatcherListener(QueueConnection connection) {
        super();
        this.connection = connection;
    }

    @Override
    public void onMessage(Message message) {

        TextMessage textMessage = (TextMessage) message;

        Thread thread = new DispatcherThread(connection, textMessage);
        thread.start();

    }

}
