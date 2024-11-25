import numpy as np
from lava.magma.core.run_configs import Loihi1SimCfg
from lava.magma.core.run_conditions import RunContinuous
from lava.proc.dense.process import Dense
from lava.proc.lif.process import LIF
from lava.proc.monitor.process import Monitor
from lava.proc.io.source import RingBuffer

class SNN:
    def __init__(self, input_size=3, hidden_size=10, output_size=4):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.build_network()

    def build_network(self):
        # Input process using RingBuffer
        input_data = np.zeros((self.input_size, 1))
        self.input_process = RingBuffer(data=input_data)

        # Hidden layer of LIF neurons
        self.hidden_layer = LIF(shape=(self.hidden_size,))

        # Output layer of LIF neurons
        self.output_layer = LIF(shape=(self.output_size,))

        # Connections between layers
        self.dense1 = Dense(weights=np.random.rand(self.hidden_size, self.input_size))
        self.dense2 = Dense(weights=np.random.rand(self.output_size, self.hidden_size))

        # Connecting the processes
        self.input_process.s_out.connect(self.dense1.s_in)
        self.dense1.a_out.connect(self.hidden_layer.a_in)
        self.hidden_layer.s_out.connect(self.dense2.s_in)
        self.dense2.a_out.connect(self.output_layer.a_in)

        # Monitor to record output spikes
        self.monitor = Monitor()
        self.monitor.probe(target=self.output_layer.s_out, num_steps=1)

        # Run configuration
        self.run_condition = RunContinuous()
        self.run_config = Loihi1SimCfg(select_tag='floating_pt')

    def start(self):
        # Start the network
        self.input_process.run(condition=self.run_condition, run_cfg=self.run_config)

    def stop(self):
        # Stop the network
        self.input_process.stop()

    def set_input(self, input_data):
        # Update the input data in the RingBuffer
        self.input_process.data.set(input_data)

    def get_output(self):
        # Retrieve the output spikes from the monitor
        data = self.monitor.get_data()
        spikes = data[self.output_layer.name]['s_out']
        return spikes
