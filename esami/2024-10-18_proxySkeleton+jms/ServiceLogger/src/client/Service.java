package client;

import java.util.HashMap;
import java.util.Random;
import java.util.concurrent.TimeUnit;

import logging.LogType;

public class Service {

    private static final int NUM_RICHIESTE = 10;

    private static final HashMap<LogType, String[]> LOGTYPE_MESSAGES = new HashMap<LogType, String[]>() {
        {
            put(LogType.DEBUG, new String[] { "success", "checking" });
            put(LogType.INFO, new String[] { "success", "checking" });
            put(LogType.ERROR, new String[] { "fatal", "exception" });
        }
    };

    private static final Random rand = new Random();

    private static <T> T getRandomValueOfArray(T[] array) {
        return array[rand.nextInt(array.length)];
    }

    public static void main(String[] args) {
        String host = null;
        int port = -1;

        if (args.length == 1) {
            host = "localhost";
            port = Integer.parseInt(args[0]);
        } else if (args.length >= 2) {
            host = args[0];
            port = Integer.parseInt(args[1]);
        } else {
            System.out.println(
                    "Inserisci il numero di porta del logging server (default host = 'localhost'), oppure l'host seguito dal numero di porta");
            System.exit(1);
            return;
        }

        LoggingProxy proxy = new LoggingProxy(host, port);

        for (int i = 0; i < NUM_RICHIESTE; i++) {
            LogType tipo = getRandomValueOfArray(LogType.values());
            String messaggioLog = getRandomValueOfArray(LOGTYPE_MESSAGES.get(tipo));

            System.out.printf("[SERVICE] Effettuo un log del messaggio '%s' di tipo %s (%d)\n",
                    messaggioLog,
                    tipo.toString(),
                    tipo.getIntValue());
            proxy.log(messaggioLog, tipo);

            try {
                TimeUnit.SECONDS.sleep(2);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
