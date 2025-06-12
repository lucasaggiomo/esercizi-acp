package dispatcher;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.Socket;

public class DispatcherProxy implements IDispatcherService {

    private final String address;
    private final int port;

    public DispatcherProxy(String address, int port) {
        this.address = address;
        this.port = port;
    }

    @Override
    public int preleva() {
        try (Socket socket = new Socket(InetAddress.getByName(address), port);
            DataOutputStream outputStream = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));
            BufferedReader inputReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));) {

            inputReader.readLine();

        } catch (

        IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        return 0;
    }

    @Override
    public void deposita(int ID) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'deposita'");
    }

}
