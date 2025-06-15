package extractor;

import javax.jms.Connection;
import javax.jms.Destination;
import javax.jms.MapMessage;
import javax.jms.Message;
import javax.jms.MessageListener;

public class ExtractorDataListener implements MessageListener {

    private final Connection connection;
    private final Destination tempDestination;
    private final Destination pressDestination;

    public ExtractorDataListener(Connection connection, Destination tempDestination, Destination pressDestination) {
        this.connection = connection;
        this.tempDestination = tempDestination;
        this.pressDestination = pressDestination;
    }

    @Override
    public void onMessage(Message message) {
        MapMessage mapMessage = (MapMessage) message;

        Thread thread = new ExtractorDataThread(mapMessage, connection, tempDestination, pressDestination);
        thread.start();
    }

}
