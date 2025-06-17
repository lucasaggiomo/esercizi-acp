package magazzino.server;

import coda.ICoda;
import io.grpc.stub.StreamObserver;
import magazzino.grpc.Articolo;
import magazzino.grpc.Empty;
import magazzino.grpc.MagazzinoServiceGrpc.MagazzinoServiceImplBase;
import magazzino.grpc.StringMessage;

public class MagazzinoServicerImpl extends MagazzinoServiceImplBase {

    private final ICoda coda;

    public MagazzinoServicerImpl(ICoda coda) {
        super();
        this.coda = coda;
    }

    @Override
    public void deposita(Articolo request, StreamObserver<StringMessage> responseObserver) {
        int id = request.getId();

        System.out.printf("[SERVICER] Ricevuta richiesta di deposito dell'articolo %d\n", id);
        coda.deposita(id);

        String rispostaText = "ACK";

        StringMessage risposta = StringMessage.newBuilder().setValue(rispostaText).build();
        System.out.printf(" [SERVICER] Invio la risposta '%s'\n", risposta.getValue());
        responseObserver.onNext(risposta);
        responseObserver.onCompleted();
    }

    @Override
    public void preleva(Empty request, StreamObserver<Articolo> responseObserver) {
        System.out.printf("[SERVICER] Ricevuta richiesta di prelievo\n");
        int id = coda.preleva();

        Articolo articolo = Articolo.newBuilder().setId(id).build();
        System.out.printf(" [SERVICER] Invio l'articolo con id '%d'\n", articolo.getId());
        responseObserver.onNext(articolo);
        responseObserver.onCompleted();
    }

}
