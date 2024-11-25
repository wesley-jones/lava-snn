# test_zmq.py

import zmq
import time
import numpy as np


def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    while True:
        # Simulate lidar data
        left = np.random.uniform(0, 10)
        center = np.random.uniform(0, 10)
        right = np.random.uniform(0, 10)
        message = f"{left},{center},{right}"
        print(f"Sending lidar data: {message}")
        socket.send_string(message)
        time.sleep(1)


if __name__ == '__main__':
    main()
