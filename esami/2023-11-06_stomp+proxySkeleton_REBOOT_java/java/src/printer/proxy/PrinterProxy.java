package printer.proxy;

import printer.IPrinter;

public abstract class PrinterProxy implements IPrinter {
    protected final String host;
    protected final int port;

    public PrinterProxy(String host, int port) {
        this.host = host;
        this.port = port;
    }

}
