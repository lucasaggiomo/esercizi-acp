package printer.proxy;

import client.proxy.PrinterProxyUDP;

public class PrinterProxyFactoryUDP implements IPrinterProxyFactory {

    @Override
    public PrinterProxy create(String host, int port) {
        return new PrinterProxyUDP(host, port);
    }

}
