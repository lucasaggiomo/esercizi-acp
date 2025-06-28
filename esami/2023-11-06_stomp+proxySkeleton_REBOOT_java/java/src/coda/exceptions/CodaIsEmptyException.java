package coda.exceptions;

public class CodaIsEmptyException extends Exception {
    public CodaIsEmptyException() {
        super();
    }

    public CodaIsEmptyException(String message) {
        super(message);
    }
}
