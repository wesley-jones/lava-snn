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
from lava.magma.core.model.py.type import LavaPyType
from config_utils import get_port_from_config

class HazardInputNode(AbstractProcess):
    def __init__(self):
        super().__init__()
        self.s_out = OutPort(shape=(2,))  # Forward spikes to 2 input nodes

@implements(proc=HazardInputNode, protocol=LoihiProtocol)
@requires(CPU)
class HazardInputNodeModel(PyLoihiProcessModel):
    s_out: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, bool, precision=1)  # Output port declaration

    def __init__(self, proc_params):
        super().__init__(proc_params)
        port = get_port_from_config("hazard_sensor")
        self.socket = zmq.Context().socket(zmq.SUB)
        self.socket.connect(f"tcp://localhost:{port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        print(f"Starting listener on port {port}")

    def run_spk(self):
        """Receive data and send spikes to two input nodes."""
        if self.socket.poll(timeout=10):  # Non-blocking receive
            message = self.socket.recv_string()
            print(f"Received hazard data: {message}")  # Log the raw message

            # Map hazard types to 2-node spikes (cliff -> Node 0, bump -> Node 1)
            match message:
                case "cliff":
                    spikes = np.array([1, 0])  # Spike for Node 0 (Cliff Input Node)
                case "bump":
                    spikes = np.array([0, 1])  # Spike for Node 1 (Bump Input Node)
                case _:
                    spikes = np.array([0, 0])  # No spikes for unknown or unhandled hazards

            print(f"Generated spikes: {spikes}")  # Log generated spikes

            # Send the spikes to the two input nodes
            self.s_out.send(spikes)

