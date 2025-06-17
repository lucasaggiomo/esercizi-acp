package server;

import javax.jms.Connection;
import javax.jms.Destination;

import logging.LogType;

public class LoggingImpl extends LoggingSkeleton {

    private final Connection connection;
    private final Destination errorDest;
    private final Destination infoDest;

    // il paradigma proxy skeleton per ereditarietà mi impone che l'impl debba
    // richiedere nel costruttore la porta, rendendo l'implementazione a conoscenza
    // di informazioni riguardo la connessione di rete (delegate-like is way better)
    public LoggingImpl(int port, Connection connection, Destination errorDest, Destination infoDest) {
        super(port);
        this.connection = connection;
        this.errorDest = errorDest;
        this.infoDest = infoDest;
    }

    @Override
    public synchronized void log(String messaggioLog, LogType tipo) {
        Destination destination = null;

        switch (tipo) {
            case DEBUG:
            case INFO:
                destination = infoDest;
                System.out.printf("         [LOGGING_IMPL] Invio il messaggio '%s' di tipo %s (%d) sulla coda info\n",
                        messaggioLog,
                        tipo.toString(),
                        tipo.getIntValue());
                break;
            case ERROR:
                destination = errorDest;
                System.out.printf("         [LOGGING_IMPL] Invio il messaggio '%s' di tipo %s (%d) sulla coda error\n",
                        messaggioLog,
                        tipo.toString(),
                        tipo.getIntValue());
                break;
        }

        Thread thread = new LoggingImplThread(messaggioLog, tipo, connection, destination);
        thread.start();
    }

}
