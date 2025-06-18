package client;

import printer.TipoStampa;
import printer.proxy.IPrinterProxyFactory;
import printer.proxy.PrinterProxy;

public class UserThread extends Thread {
    private final String host;
    private final int port;
    private final IPrinterProxyFactory proxyFactory;

    private final String pathFile;
    private final TipoStampa tipo;

    public UserThread(
            String name,
            String host,
            int port,
            IPrinterProxyFactory proxyFactory,
            String pathFile,
            TipoStampa tipo) {
        super(name);
        this.host = host;
        this.port = port;
        this.proxyFactory = proxyFactory;
        this.pathFile = pathFile;
        this.tipo = tipo;
    }

    @Override
    public void run() {
        System.out.printf("[USER-THREAD-%s] Invio la richiesta di print del file %s con tipo %s\n",
                this.getName(),
                pathFile,
                tipo.toString());

        // crea il proxy
        PrinterProxy proxy = proxyFactory.create(host, port);
        proxy.print(pathFile, tipo);
    }

}
