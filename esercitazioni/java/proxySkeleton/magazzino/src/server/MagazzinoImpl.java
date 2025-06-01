package server;

import coda.Coda;
import coda.concurrent.CodaSemaphores;
import coda.impl.CodaCircolare;
import magazzino.Articolo;
import magazzino.IMagazzino;

public class MagazzinoImpl implements IMagazzino {

    private Coda[] codeArticoli;

    public MagazzinoImpl(int capacity) {
        codeArticoli = new Coda[Articolo.values().length];
        for (int i = 0; i < Articolo.values().length; i++) {
            // nota: è possibile separare anche 'istanziazione dalla logica di utilizzo
            // attraverso un "Factory":
            // codeArticoli[i] = CodaFactory.creaCoda(tipoDiCoda);
            // dove tipoDiCoda magari è un enum che indica il tipo di coda da creare, che
            // viene dato dall'esterno o qualcosa del genere
            Coda coda = new CodaCircolare(capacity);
            codeArticoli[i] = new CodaSemaphores(coda);
        }
    }

    private Coda getCoda(Articolo articolo) {
        return codeArticoli[articolo.ordinal()];
    }

    @Override
    public void deposita(Articolo articolo, int id) {
        Coda coda = getCoda(articolo);
        coda.deposita(id);

        System.out.printf("[MAGAZZINO IMPL] Ho depositato l'articolo %s con id %d\n", articolo.toString(), id);
    }

    @Override
    public int preleva(Articolo articolo) {
        Coda coda = getCoda(articolo);

        int id = coda.preleva();

        System.out.printf("[MAGAZZINO IMPL] Ho prelevato l'articolo %s con id %d\n", articolo.toString(), id);

        return id;
    }

}
