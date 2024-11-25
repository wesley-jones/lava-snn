# zmq_receiver.py

import zmq


class ZmqReceiver:
    def __init__(self, host='localhost', port=5555):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{host}:{port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def receive(self):
        message = self.socket.recv_string()
        # Assuming the message is a string of numbers separated by commas
        data = [float(x) for x in message.split(',')]
        return data
