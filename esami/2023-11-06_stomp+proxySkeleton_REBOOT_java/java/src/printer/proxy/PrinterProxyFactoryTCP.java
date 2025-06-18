package printer.proxy;

import client.proxy.PrinterProxyTCP;

public class PrinterProxyFactoryTCP implements IPrinterProxyFactory {

    @Override
    public PrinterProxy create(String host, int port) {
        return new PrinterProxyTCP(host, port);
    }

}
