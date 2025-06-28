package magazzino;

public interface IMagazzino {

    public void deposita(Articolo articolo, int id);

    public int preleva(Articolo articolo);

}
