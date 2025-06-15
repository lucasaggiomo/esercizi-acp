import stomp
from stomp.utils import Frame
import multiprocessing as mp
from utils import set_string, get_string

STATS_STRING = "Sold"


class StatsListener(stomp.ConnectionListener):
    def __init__(
        self,
        queue: mp.Queue,
    ):
        super().__init__()
        self.queue = queue

    def statsFun(self):
        artists = []

        while not self.queue.empty():
            artist = self.queue.get()
            artists.append(artist)

        artistStats: dict[str, int] = {}

        for artist in artists:
            if artist not in artistStats.keys():
                artistStats[artist] = 1
            else:
                artistStats[artist] += 1

        with open("stats.txt", mode="a") as file:
            for artist, numSells in artistStats.items():
                line = f"{artist}: {numSells}"
                file.write(line + "\n")
                print(
                    "         [STATS_LISTENER_THREAD] Aggiungo "
                    + line
                    + " al file stats.txt"
                )

    def on_message(self, frame: Frame):
        message = frame.body

        print(f"[STATS_LISTENER] Ho letto il messagggio {message}")
        if message != STATS_STRING:
            print("[STATS_LISTENER] Il messaggio non è " + STATS_STRING + "!")
            return

        process = mp.Process(target=self.statsFun, args=())
        process.start()


class TicketsListener(stomp.ConnectionListener):
    def __init__(
        self,
        queue: mp.Queue,
    ):
        super().__init__()
        self.queue = queue

    def ticketsFun(self, artist: str):
        self.queue.put(artist)
        print(f"        [TICKETS_LISTENER_THREAD] Ho aggiunto l'artista {artist}")

    def on_message(self, frame: Frame):
        message = frame.body

        print(f"[TICKETS_LISTENER] Ho letto il messagggio {message}")

        process = mp.Process(target=self.ticketsFun, args=(message,))
        process.start()
