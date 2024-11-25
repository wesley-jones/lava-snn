# zmq_sender.py

import zmq


class ZmqSender:
    def __init__(self, port=5556):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")

    def send(self, data):
        # If data is a string or list of strings
        if isinstance(data, list):
            message = ','.join(map(str, data))
        else:
            message = str(data)
        self.socket.send_string(message)
