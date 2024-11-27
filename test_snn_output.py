# read_snn_output.py

import zmq
from config_utils import get_port_from_config

def main():
    port = get_port_from_config("velocity_command")
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{port}")  # Connect to the SNN's publisher port
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
