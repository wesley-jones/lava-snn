from turtlebot_snn import TurtleBotSNN
from lava.magma.core.run_configs import Loihi1SimCfg
from lava.magma.core.run_conditions import RunContinuous
from lava.magma.core.run_conditions import RunSteps

def main():
    # Initialize the composite system
    turtlebot_snn = TurtleBotSNN()

    # Define run configuration
    run_condition = RunContinuous()
    # run_condition = RunSteps(num_steps=1000)  # Run for 1000 steps
    run_config = Loihi1SimCfg()

    print("Starting the Lava SNN... (Press Ctrl+C to stop)")
    turtlebot_snn.run(condition=run_condition, run_cfg=run_config)

if __name__ == "__main__":
    main()
