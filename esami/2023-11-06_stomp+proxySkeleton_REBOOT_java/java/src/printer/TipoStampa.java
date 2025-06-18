package printer;

public enum TipoStampa {
    BIANCO_NERO("bw"),
    SCALA_GRIGI("gs"),
    COLOR("color");

    private final String name;

    private TipoStampa(String name) {
        this.name = name;
    }

    public static TipoStampa fromName(String name) throws IllegalArgumentException {
        TipoStampa[] tipi = TipoStampa.values();
        for (TipoStampa tipo : tipi) {
            if (tipo.name.equals(name)) {
                return tipo;
            }
        }
        throw new IllegalArgumentException("Non esiste un TipoStampa con nome " + name);
    }

    @Override
    public String toString() {
        return this.name;
    }
}
