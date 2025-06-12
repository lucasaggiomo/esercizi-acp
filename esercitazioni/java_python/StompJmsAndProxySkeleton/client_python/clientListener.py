import stomp


class ClientListener(stomp.ConnectionListener):

    def on_message(self, frame):
        print("[CLIENT LISTENER] Ricevuto " + str(frame.body))
