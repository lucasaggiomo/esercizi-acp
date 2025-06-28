package printer.skeleton;

import printer.IPrinter;
import printer.TipoStampa;

public abstract class PrinterSkeleton implements IPrinter {
    protected int port;
    protected IPrinter printer;

    public PrinterSkeleton(IPrinter printer) {
        this(0, printer);
    }

    public PrinterSkeleton(int port, IPrinter printer) {
        this.printer = printer;
        this.port = port;
    }

    @Override
    public void print(String pathFile, TipoStampa tipo) {
        printer.print(pathFile, tipo);
    }

    public abstract void runSkeleton();
}
