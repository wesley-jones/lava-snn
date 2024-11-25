from snn_module import SNN
from zmq_receiver import ZmqReceiver
from zmq_sender import ZmqSender
import numpy as np
import time

def main():
    # Initialize the SNN
    snn = SNN(input_size=3, hidden_size=10, output_size=4)
    snn.start()

    # Initialize ZeroMQ receiver and sender
    receiver = ZmqReceiver(host='localhost', port=5555)
    sender = ZmqSender(port=5556)

    try:
        while True:
            # Receive LiDAR data
            input_data = receiver.receive()
            print(f"Received input data: {input_data}")

            # Normalize the input data
            input_data = np.clip(input_data, 0.0, 10.0) / 10.0

            # Set the input data to the SNN
            snn.set_input(input_data)

            # Allow some time for the network to process
            time.sleep(0.1)

            # Get the output from the SNN
            output_spikes = snn.get_output()
            print(f"Output spikes: {output_spikes}")

            # Determine movement command based on output spikes
            movement_commands = ['left', 'right', 'forward', 'don\'t move']
            command_index = np.argmax(output_spikes)
            movement_command = movement_commands[command_index]

            # Send movement command via ZeroMQ
            sender.send([movement_command])
            print(f"Sent movement command: {movement_command}")

            # Sleep to simulate real-time processing
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping the SNN...")
        snn.stop()

if __name__ == '__main__':
    main()
