# test_zmq.py

import zmq
import time
import numpy as np
from config_utils import get_port_from_config


def main():
    port = get_port_from_config("lidar_sensor")
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://*:{port}")

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
