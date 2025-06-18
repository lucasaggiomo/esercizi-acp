package server;

import coda.ICoda;
import coda.exceptions.CodaIsFullException;
import printer.TipoStampa;

public class PrinterServerProduttoreThread extends Thread {

    private final ICoda<String> coda;
    private final String pathFile;
    private final TipoStampa tipo;

    public PrinterServerProduttoreThread(ICoda<String> coda, String pathFile, TipoStampa tipo) {
        this.coda = coda;
        this.pathFile = pathFile;
        this.tipo = tipo;
    }

    @Override
    public void run() {
        String item = String.format("%s-%s", pathFile, tipo.toString());
        System.out.printf("            [PRODUTTORE] Produco %s sulla coda\n", item);

        try {
            coda.push(item);
            System.out.println("             [PRODUTTORE] OK");
        } catch (CodaIsFullException e) {
            e.printStackTrace();
        }
    }

}
