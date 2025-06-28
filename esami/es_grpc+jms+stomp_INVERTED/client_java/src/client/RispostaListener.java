package client;

import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.TextMessage;
import javax.jms.MessageListener;

public class RispostaListener implements MessageListener {

    @Override
    public void onMessage(Message message) {
        try {
            System.out.println("    [LISTENER] Ho ricevuto il messaggio " + ((TextMessage) message).getText());
        } catch (JMSException e) {
            e.printStackTrace();
        }
    }

}
