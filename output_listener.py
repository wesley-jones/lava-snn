# output_listener.py

import zmq


def main():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        message = socket.recv_string()
        print(f"Received movement command: {message}")


if __name__ == '__main__':
    main()
