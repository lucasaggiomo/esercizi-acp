package server;

import magazzino.Articolo;
import magazzino.IMagazzino;

public abstract class MagazzinoSkeleton implements IMagazzino {
    protected final IMagazzino magazzino;

    public MagazzinoSkeleton(IMagazzino magazzino) {
        this.magazzino = magazzino;
    }

    @Override
    public void deposita(Articolo articolo, int id) {
        this.magazzino.deposita(articolo, id);
    }

    @Override
    public int preleva(Articolo articolo) {
        return this.magazzino.preleva(articolo);
    }

    public abstract void runSkeleton();

}
