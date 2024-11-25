import zmq
import numpy as np
from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
from lava.magma.core.resources import CPU
from lava.magma.core.decorator import implements, requires
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.process.ports.ports import OutPort
from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.model.py.ports import PyOutPort
from lava.magma.core.process.variable import Var
from lava.magma.core.model.py.type import LavaPyType


class ListenerNode(AbstractProcess):
    def __init__(self):
        super().__init__()
        self.s_out = OutPort(shape=(3,))  # Forward spikes to 3 input nodes

@implements(proc=ListenerNode, protocol=LoihiProtocol)
@requires(CPU)
class ListenerNodeModel(PyLoihiProcessModel):
    s_out: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, bool, precision=1)  # Output port declaration

    def __init__(self, proc_params):
        super().__init__(proc_params)
        self.socket = zmq.Context().socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5555")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        print("Starting listener on port 5555")

    def run_spk(self):
        """Receive data and send spikes."""
        # print("Running listener run_spk method...")  # Log method execution
        if self.socket.poll(timeout=10):  # Non-blocking receive
            message = self.socket.recv_string()
            print(f"Received lidar data: {message}")  # Log the raw message
            lidar_data = np.array([float(x) for x in message.split(',')])
            print(f"Parsed lidar data: {lidar_data}")  # Log parsed data
            spikes = (lidar_data > 0.01).astype(int)  # Threshold example for spikes
            print(f"Generated spikes from lidar: {spikes}")  # Log generated spikes
            self.s_out.send(spikes)

        # else:
            # spikes = np.array([0, 0, 0])
            # self.s_out.send(spikes)
            # print("No lidar data.")  # Log if no messages are received

        # while True:  # Continuous loop within run_spk
        #     print("Listening for messages...")
        #     if self.socket.poll(timeout=10):  # Non-blocking receive
        #         message = self.socket.recv_string()
        #         print(f"Received message: {message}")
        #         lidar_data = np.array([float(x) for x in message.split(',')])
        #         spikes = (lidar_data > 1.0).astype(int)
        #         self.s_out.send(spikes)
        #     else:
        #         print("No messages received.")
