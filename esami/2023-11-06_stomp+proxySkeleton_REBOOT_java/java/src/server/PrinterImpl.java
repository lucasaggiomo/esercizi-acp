package server;

import coda.ICoda;
import printer.IPrinter;
import printer.TipoStampa;

public class PrinterImpl implements IPrinter {

    private final ICoda<String> coda;

    public PrinterImpl(ICoda<String> coda) {
        this.coda = coda;
    }

    @Override
    public void print(String pathFile, TipoStampa tipo) {
        Thread th = new PrinterServerProduttoreThread(coda, pathFile, tipo);
        th.start();
    }

}
