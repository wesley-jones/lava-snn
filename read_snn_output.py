# read_snn_output.py

import zmq


def main():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")  # Connect to the SNN's publisher port
    socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

    print("Listening for SNN output...")
    try:
        while True:
            message = socket.recv_string()  # Receive output from the SNN
            print(f"Received command from SNN: {message}")
    except KeyboardInterrupt:
        print("\nStopping output listener.")
    finally:
        socket.close()
        context.term()


if __name__ == '__main__':
    main()
