import sys

import stomp


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


@static_vars(counter=0)
def getFromArgvOrDefault(default, type: type = str):
    getFromArgvOrDefault.counter += 1
    index = getFromArgvOrDefault.counter
    if len(sys.argv) > index:
        return type(sys.argv[index])
    return default


if __name__ == "__main__":
    ADDRESS = getFromArgvOrDefault("127.0.0.1")
    PORT = getFromArgvOrDefault(61613, int)
    print(f"Address: {ADDRESS}, Port: {PORT}")

    conn = stomp.Connection([(ADDRESS, PORT)])
    conn.connect(wait=True)

    conn.send("/queue/giovanni", "Giovanni")

    conn.disconnect()
