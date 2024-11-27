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

class LidarInputNode(AbstractProcess):
    def __init__(self):
        super().__init__()
        self.s_out = OutPort(shape=(3,))  # Forward spikes to 3 input nodes

@implements(proc=LidarInputNode, protocol=LoihiProtocol)
@requires(CPU)
class LidarInputNodeModel(PyLoihiProcessModel):
    s_out: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, bool, precision=1)  # Output port declaration

    def __init__(self, proc_params):
        super().__init__(proc_params)
        port = get_port_from_config("lidar_sensor")
        self.socket = zmq.Context().socket(zmq.SUB)
        self.socket.connect(f"tcp://localhost:{port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        print(f"Starting listener on port {port}")

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
