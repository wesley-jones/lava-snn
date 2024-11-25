import zmq
import numpy as np
from lava.magma.core.process.ports.ports import InPort
from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.process.variable import Var
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.model.py.ports import PyInPort
from lava.magma.core.decorator import implements, requires
from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
from lava.magma.core.resources import CPU
from lava.magma.core.model.py.type import LavaPyType

class PublisherNode(AbstractProcess):
    def __init__(self):
        super().__init__()
        self.s_in = InPort(shape=(1,))  # Listen to 4 output neurons

@implements(proc=PublisherNode, protocol=LoihiProtocol)  # Link ProcessModel to PublisherNode
@requires(CPU)  # Specify that this ProcessModel runs on the CPU
class PublisherNodeModel(PyLoihiProcessModel):
    s_in: PyInPort = LavaPyType(PyInPort.VEC_DENSE, bool, precision=1)  # Input port declaration

    def __init__(self, proc_params):
        super().__init__(proc_params)
        self.socket = zmq.Context().socket(zmq.PUB)
        self.socket.setsockopt(zmq.SNDHWM, 1)  # Set the send high-water mark to 1
        self.socket.bind("tcp://*:5556")
        self.count = 0
        print(f"Counter: {self.count}")

    def run_spk(self):
        """Send spikes as ZeroMQ messages."""
        print(f"Counter: {self.count}")
        # print("run_spk: Publisher Node")  # Log if no messages are received
        if self.count < 111:
            print(f"Counter: {self.count}")
            if self.s_in.probe() is True:
                spikes = self.s_in.recv()  # Receive spikes from connected neurons
                if np.any(spikes):  # Check if any output neuron spiked
                    command = ["left", "right", "forward", "stop"][np.argmax(spikes)]
                    print(f"Sending next command: {command}")
                    self.socket.send_string(command)
                    self.count += 1
