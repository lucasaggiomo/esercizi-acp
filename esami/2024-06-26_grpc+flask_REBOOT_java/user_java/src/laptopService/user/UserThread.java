package laptopService.user;

import laptopService.grpc.Empty;
import laptopService.grpc.Laptop;
import laptopService.grpc.StringMessage;
import laptopService.grpc.LaptopServiceGrpc.LaptopServiceBlockingStub;

public class UserThread extends Thread {

    private final TipoRichiesta tipo;
    private int serialNumber;
    private final LaptopServiceBlockingStub laptopService;

    public UserThread(String name, LaptopServiceBlockingStub laptopService, TipoRichiesta tipo) {
        super(name);
        this.tipo = tipo;
        this.laptopService = laptopService;
    }

    public UserThread(String name, LaptopServiceBlockingStub laptopService, TipoRichiesta tipo, int serialNumber) {
        this(name, laptopService, tipo);
        this.serialNumber = serialNumber;
    }

    @Override
    public void run() {
        Laptop laptop = null;
        switch (tipo) {
            case ACQUISTO:
                System.out.printf("     [USER-THREAD-%s] Effettuo un acquisto...\n", this.getName());

                Empty empty = Empty.newBuilder().build();
                laptop = laptopService.buy(empty);
                serialNumber = laptop.getSerialNumber();

                System.out.printf("         [USER-THREAD-%s] Ho acquistato il laptop %d\n", this.getName(), serialNumber);
                break;

            case VENDITA:
                System.out.printf("     [USER-THREAD-%s] Effettuo la vendita del laptop %d...\n",
                        this.getName(),
                        serialNumber);

                laptop = Laptop.newBuilder().setSerialNumber(serialNumber).build();
                StringMessage message = laptopService.sell(laptop);

                System.out.printf("         [USER-THREAD-%s] Ho ricevuto il messaggio %s\n", this.getName(),
                        message.getValue());

                break;
        }
    }

}
