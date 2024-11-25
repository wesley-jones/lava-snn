import zmq
from lava.magma.core.process.ports.ports import InPort
from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.model.py.ports import PyInPort
from lava.magma.core.decorator import implements, requires
from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
from lava.magma.core.resources import CPU
from lava.magma.core.model.py.type import LavaPyType


class LoggerNode(AbstractProcess):
    def __init__(self, shape):
        super().__init__()
        self.s_in = InPort(shape=shape)  # Listen to spikes


@implements(proc=LoggerNode, protocol=LoihiProtocol)
@requires(CPU)
class LoggerNodeModel(PyLoihiProcessModel):
    s_in: PyInPort = LavaPyType(PyInPort.VEC_DENSE, bool, precision=1)

    def run_spk(self):
        """Log spiking activity in real-time."""
        spikes = self.s_in.recv()  # Receive spikes
        print(f"Real-Time Spikes: {spikes}")
