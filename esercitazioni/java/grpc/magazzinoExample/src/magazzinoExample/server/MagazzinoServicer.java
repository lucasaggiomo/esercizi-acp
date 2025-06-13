package magazzinoExample.server;

import coda.Coda;
import coda.CodaCircolare;
import coda.CodaConditionsWrapper;
import coda.CodaIsEmptyException;
import coda.CodaIsFullException;
import coda.CodaQueue;
import coda.CodaSemaphoresWrapper;
import coda.CodaSynchrWrapper;
import magazzinoExample.magazzino.Acknowledge;
import magazzinoExample.magazzino.Articolo;
import magazzinoExample.magazzino.Empty;
import magazzinoExample.magazzino.MagazzinoGrpc.MagazzinoImplBase;
import io.grpc.stub.StreamObserver;

public class MagazzinoServicer extends MagazzinoImplBase {
    private Coda<Long> coda;

    public MagazzinoServicer(int capacity) {
        super();
        this.coda = new CodaSemaphoresWrapper<>(new CodaQueue<>(capacity));
    }

    @Override
    public void deposita(Articolo request, StreamObserver<Acknowledge> responseObserver) {
        // gestisce la richiesta
        long id = request.getId();
        System.out.println("[SERVICER] Deposito " + id);
        String response = "";
        try {
            coda.push(id);
            response = "ACK";
            System.out.println("[SERVICER] Ho depositato " + id + ", mando: " + response);
        } catch (CodaIsFullException e) {
            response = "ERROR: " + e.getMessage();
            System.out.println("[SERVICER] Errore nel deposito di " + id + ", mando: " + response);
        }

        // risponde al client
        Acknowledge ack = Acknowledge.newBuilder().setMessage(response).build();
        responseObserver.onNext(ack);
        responseObserver.onCompleted();
    }

    @Override
    public void preleva(Empty request, StreamObserver<Articolo> responseObserver) {
        // gestisce la richiesta
        System.out.println("[SERVICER] Prelievo");
        long id;
        try {
            id = coda.pop();
            System.out.println("[SERVICER] Ho prelevato " + id);
        } catch (CodaIsEmptyException e) {
            id = -1;
            System.out.println("[SERVICER] Errore nel preleva, mando -1: " + e.getMessage());
        }

        // risponde al client
        Articolo articolo = Articolo.newBuilder().setId(id).build();
        responseObserver.onNext(articolo);
        responseObserver.onCompleted();
    }

}
