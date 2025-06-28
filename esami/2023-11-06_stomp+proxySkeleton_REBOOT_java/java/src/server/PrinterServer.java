package server;

import java.util.Hashtable;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

import coda.CodaCircolare;
import coda.ICoda;
import coda.concurrent.CodaConditionsWrapper;
import printer.IPrinter;
import printer.skeleton.PrinterSkeleton;
import server.skeleton.tcp.PrinterSkeletonTCP;
import server.skeleton.udp.PrinterSkeletonUDP;

public class PrinterServer {

    private static final int PORT = 0;

    private static final int DIM_CODA = 5;

    public static void main(String[] args) {
        Hashtable<String, String> prop = new Hashtable<>();
        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("queue.bw", "bw");
        prop.put("queue.color", "color");

        try {
            Context context = new InitialContext(prop);

            ConnectionFactory factory = (ConnectionFactory) context.lookup("QueueConnectionFactory");
            Destination destBW = (Destination) context.lookup("bw");
            Destination destCOLOR = (Destination) context.lookup("color");

            Connection connection = factory.createConnection();

            ICoda<String> coda = new CodaConditionsWrapper<>(new CodaCircolare<>(DIM_CODA));

            Thread consumatore = new PrinterServerConsumatoreThread(coda, connection, destBW, destCOLOR);
            consumatore.start();

            IPrinter printer = new PrinterImpl(coda);
            PrinterSkeleton skeleton = new PrinterSkeletonUDP(PORT, printer);
            skeleton.runSkeleton();

            try {
                consumatore.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            connection.close();

        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }
    }
}
