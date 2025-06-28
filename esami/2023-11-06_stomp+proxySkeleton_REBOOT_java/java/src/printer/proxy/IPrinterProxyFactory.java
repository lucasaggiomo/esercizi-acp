package printer.proxy;

@FunctionalInterface
public interface IPrinterProxyFactory {
    PrinterProxy create(String host, int port);
}
