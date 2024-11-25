from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.process.ports.ports import OutPort, InPort
from lava.magma.core.decorator import implements, requires
from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
from lava.magma.core.run_conditions import RunSteps
from lava.magma.core.run_configs import Loihi1SimCfg
from lava.magma.core.resources import CPU
from lava.magma.core.model.py.ports import PyInPort, PyOutPort
from lava.magma.core.model.py.type import LavaPyType
from lava.magma.core.run_conditions import RunContinuous


class TestNode(AbstractProcess):
    def __init__(self):
        super().__init__()
        self.s_out = OutPort(shape=(1,))


@implements(proc=TestNode, protocol=LoihiProtocol)
@requires(CPU)
class TestNodeModel(PyLoihiProcessModel):
    s_out: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, bool, precision=1)

    def run_spk(self):
        print("run_spk executed")


def main():
    node = TestNode()
    run_condition = RunContinuous()
    # run_condition = RunSteps(num_steps=15)
    node.run(condition=run_condition, run_cfg=Loihi1SimCfg())


if __name__ == "__main__":
    main()
