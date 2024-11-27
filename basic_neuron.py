import numpy as np
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.model.py.ports import PyInPort, PyOutPort
from lava.magma.core.decorator import implements, requires
from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
from lava.magma.core.resources import CPU
from lava.magma.core.process.ports.ports import OutPort
from lava.magma.core.process.ports.ports import InPort
from lava.magma.core.model.py.type import LavaPyType
from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.process.variable import Var


# Define the Basic Neuron Process
class BasicNeuron(AbstractProcess):
    def __init__(self, threshold=1.0):
        super().__init__()
        self.s_in = InPort(shape=(3,))  # Single input port
        self.s_out = OutPort(shape=(1,))  # Single output port
        # self.v_mem = Var(shape=(1,), init=0.0)  # Declare membrane potential


# Implement the ProcessModel for the Basic Neuron
@implements(proc=BasicNeuron, protocol=LoihiProtocol)
@requires(CPU)
class BasicNeuronModel(PyLoihiProcessModel):
    s_in: PyInPort = LavaPyType(PyInPort.VEC_DENSE, bool, precision=1)
    s_out: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, bool, precision=1)
    # v_mem: float = LavaPyType(float, float)  # Membrane potential

    def __init__(self, proc_params):
        super().__init__(proc_params)
        # self.threshold = 1.0  # Hard-code the threshold here
        # self.v_mem = 0  # Initialize membrane potential

    def run_spk(self):
        # Non-blocking check for input
        if self.s_in.probe() is True:
            input_spikes = self.s_in.recv()
            print(f"BasicNeuron received spikes: {input_spikes}")
            fire_spike = np.any(input_spikes)  # Fire if any input is True
            # Update membrane potential
            # self.v_mem += input_spikes
            # self.s_out.send(fire_spike)
            self.s_out.send(np.array([fire_spike], dtype=bool))
        # else:
        #     print("No input spikes received, skipping computation.")

        # Check if the neuron fires
        # fire_spike = self.v_mem > self.threshold
        # print(f"BasicNeuron is firing spike: {fire_spike}")
        # if fire_spike:
            # self.s_out.send(fire_spike)
            # Reset membrane potential for fired neurons
            # self.v_mem[fire_spike] = 0

