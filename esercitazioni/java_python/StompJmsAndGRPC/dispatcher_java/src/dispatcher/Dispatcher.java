// Dispatcher (Java). Questa entità funge da intermediario tra le richieste inviate dal
// client al server. Il dispatcher si occupa di prelevare le richieste del client dalla coda
// Richiesta (gestita con STOMP), e le inoltra al Server. Il dispatcher è
// un’applicazione multithread che riceve in maniera asincrona le richieste da parte di
// Client sulla coda Richiesta, ne estrae le informazioni (tipo richiesta, valore), ed
// invoca (attraverso un nuovo thread) il corrispondente metodo preleva o deposita
// fornito da Server attraverso gRPC (Dispatcher funge da client gRPC verso Server).

package dispatcher;

import java.util.Hashtable;
// import java.util.concurrent.TimeUnit;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageConsumer;
import javax.jms.Session;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

import dispatcher.magazzino.MagazzinoGrpc;
import dispatcher.magazzino.MagazzinoGrpc.MagazzinoBlockingStub;
import io.grpc.Grpc;
import io.grpc.InsecureChannelCredentials;
import io.grpc.ManagedChannel;

public class Dispatcher {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.err.println(
                    "Inserisci solo numero di porta del server python se l'indirizzo è 'localhost', oppure l'indirizzo e il numero di porta");
            System.exit(1);
            return;
        }

        String HOST_GRPC = args.length >= 2 ? args[0] : "localhost";
        int PORT_GRPC = Integer.parseInt(args[args.length == 1 ? 0 : 1]);

        Hashtable<String, String> prop = new Hashtable<>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("queue.richiesta", "richiesta");

        try {
            Context context = new InitialContext(prop);

            ConnectionFactory factory = (ConnectionFactory) context.lookup("QueueConnectionFactory");
            Connection connection = factory.createConnection();
            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            Destination destination = (Destination) context.lookup("richiesta");
            MessageConsumer consumer = session.createConsumer(destination);

            // si connette al server python gRPC tramite lo stub
            ManagedChannel channel = Grpc
                    .newChannelBuilderForAddress(
                            HOST_GRPC, PORT_GRPC,
                            InsecureChannelCredentials.create())
                    .build();

            connection.start();

            MagazzinoBlockingStub magazzinoStub = MagazzinoGrpc.newBlockingStub(channel);
            DispatcherListener listener = new DispatcherListener(connection, magazzinoStub);
            consumer.setMessageListener(listener);

            System.out.println("[DISPATCHER] Avviato - comunicazione lato server su porto: " + PORT_GRPC);

            // Non chiude il canale altrimenti non funziona la comunicazione
            // try {
            // channel.shutdownNow().awaitTermination(60, TimeUnit.SECONDS);
            // } catch (InterruptedException e) {
            // // TODO Auto-generated catch block
            // e.printStackTrace();
            // }

        } catch (NamingException | JMSException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
