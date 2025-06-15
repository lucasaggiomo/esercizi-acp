package manager;

import javax.jms.MapMessage;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.Connection;
import javax.jms.Destination;

public class RequestListener implements MessageListener {

    private final Connection connection;
    private final Destination statsDestination;
    private final Destination ticketsDestination;

    public RequestListener(
            Connection connection,
            Destination statsDestination,
            Destination ticketsDestination) {
        super();
        this.connection = connection;
        this.statsDestination = statsDestination;
        this.ticketsDestination = ticketsDestination;
    }

    @Override
    public void onMessage(Message message) {
        MapMessage mapMessage = (MapMessage) message;

        Thread t = new ManagerThread(mapMessage, connection, statsDestination, ticketsDestination);
        t.start();
    }

}
