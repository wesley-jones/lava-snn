from lidar_input_node import LidarInputNode
from hazard_input_node import HazardInputNode
from velocity_output_node import VelocityOutputNode
from basic_neuron import BasicNeuron

class TurtleBotSNN:
    def __init__(self):
        # Lidar Input Node
        self.lidar_input_node = LidarInputNode()

        # Hazard Input Node
        self.hazard_input_node = HazardInputNode()

        # Velocity Output Node
        self.velocity_output_node = VelocityOutputNode()

        # Basic Neuron
        self.basic_neuron = BasicNeuron(threshold=1.0)

        # Connect Lidar Input Node -> Basic Neuron -> Velocity Output Node
        self.lidar_input_node.s_out.connect(self.basic_neuron.s_in)
        self.basic_neuron.s_out.connect(self.velocity_output_node.s_in)

        # List of all processes for easier management
        self.processes = [
            self.lidar_input_node,
            self.hazard_input_node,
            self.basic_neuron,
            self.velocity_output_node,
        ]

    def run(self, condition, run_cfg):
        """Run all sub-processes."""
        for process in self.processes:
            print("Starting next node")
            process.run(condition=condition, run_cfg=run_cfg)

    def stop(self):
        """Stop all sub-processes."""
        for process in self.processes:
            process.stop()
