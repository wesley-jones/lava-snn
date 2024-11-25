from listener_node import ListenerNode
from publisher_node import PublisherNode
from basic_neuron import BasicNeuron


class TurtleBotSNN:
    def __init__(self):
        # Listener Node
        self.listener = ListenerNode()

        # Input Layer (3 neurons)
        # self.input_layer = LIF(shape=(3,))

        # Hidden Layers (each with 5 neurons)
        # self.hidden_layers = [LIF(shape=(5,)) for _ in range(3)]

        # Dense Connections
        # self.dense_connections = [
        #     Dense(weights=np.random.rand(5, 3)),  # Input to first hidden layer
        #     Dense(weights=np.random.rand(5, 5)),  # First to second hidden layer
        #     Dense(weights=np.random.rand(5, 5)),  # Second to third hidden layer
        # ]

        # Output Layer (4 neurons)
        # self.output_layer = LIF(shape=(4,))
        # self.output_dense = Dense(weights=np.random.rand(4, 5))

        # Publisher Node
        self.publisher = PublisherNode()

        # Dense Layer (3 inputs -> 4 outputs)
        # self.hidden_layer = Dense(weights=np.ones((4, 3)))  # Simplified weights for testing

        # Connect Listener to Dense Layer
        # self.listener.s_out.connect(self.hidden_layer.s_in)
        # Custom Basic Neuron
        self.basic_neuron = BasicNeuron(threshold=1.0)

        # Connect Listener -> Basic Neuron -> Publisher
        self.listener.s_out.connect(self.basic_neuron.s_in)
        self.basic_neuron.s_out.connect(self.publisher.s_in)

        # Connect Dense Layer to Publisher
        # self.hidden_layer.a_out.connect(self.publisher.s_in)


        # Connect Listener to Input Layer
        # self.listener.s_out.connect(self.input_layer.a_in)

        # Connect Input Layer to First Dense Layer
        # self.input_layer.s_out.connect(self.dense_connections[0].s_in)

        # Logger node to monitor output
        # self.input_logger = LoggerNode(shape=(3,))  # Shape matches output layer size
        # self.input_layer.s_out.connect(self.input_logger.s_in)

        # Connect Hidden Layers
        # for i in range(len(self.hidden_layers)):
        #     self.dense_connections[i].a_out.connect(self.hidden_layers[i].a_in)
        #     if i < len(self.hidden_layers) - 1:  # Connect Hidden Layers sequentially
        #         self.hidden_layers[i].s_out.connect(self.dense_connections[i + 1].s_in)

        # Connect Last Hidden Layer to Output Dense Layer
        # self.hidden_layers[-1].s_out.connect(self.output_dense.s_in)

        # Connect Output Dense Layer to Output Layer
        # self.output_dense.a_out.connect(self.output_layer.a_in)

        # Connect Output Layer to Publisher
        # self.output_layer.s_out.connect(self.publisher.s_in)

        # List of all processes for easier management
        self.processes = [
            self.listener,
            self.basic_neuron,
            # self.input_layer,
            # *self.hidden_layers,
            # self.output_layer,
            self.publisher,
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
