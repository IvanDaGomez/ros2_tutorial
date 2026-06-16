# ROS 2 Tutorial: Mastering Parameters

## What are Parameters?

In ROS 2, **Parameters** act as the configuration settings for your nodes. They are structured as key-value pairs (where the key is always a string, and the value can be an integer, float, boolean, string, or an array). 

Unlike hardcoded variables, parameters can be set at startup via configuration files or **dynamically modified at runtime** via the command line or other nodes without needing to stop and restart your robot's software execution loops.

---

## The Parameter Lifecycle

For a node to interact with a parameter securely, it follows a strict lifecycle model:

1. **Declaration:** Every node must explicitly declare its parameters and their default values inside its initialization constructor. Reading or setting an undeclared parameter will throw a runtime exception.
2. **Configuration:** When booting up a node layout, default parameters can be overridden using terminal arguments or `.yaml` launch configurations.
3. **Dynamic Interception:** Nodes can register a callback tracker to intercept parameter modifications on-the-fly, allowing them to adjust hardware states or internal timers the exact millisecond a value shifts.

---

## Step-by-Step Implementation Guide

This guide will show you how to implement a complete parameter system within a standard ROS 2 Python node workspace.

### 1. Declare and Read Parameters in Your Node

Create a new file named `param_tuning_node.py` inside your application workspace module (`src/your_package/your_package/param_tuning_node.py`).

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult

class ParamTuningNode(Node):

    def __init__(self):
        super().__init__('param_tuning_node')
        
        # ==============================================================================
        # 1. PARAMETER DECLARATION (Key, Default Value)
        # ==============================================================================
        self.declare_parameter('execution_frequency', 1.0)
        self.declare_parameter('robot_safety_mode', 'standard')
        self.declare_parameter('max_linear_velocity', 0.5)

        # ==============================================================================
        # 2. INITIAL FETCHING
        # ==============================================================================
        self.frequency = self.get_parameter('execution_frequency').get_parameter_value().double_value
        self.safety_mode = self.get_parameter('robot_safety_mode').get_parameter_value().string_value
        self.max_vel = self.get_parameter('max_linear_velocity').get_parameter_value().double_value

        self.get_logger().info(f"Node started. Mode: {self.safety_mode} | Freq: {self.frequency}Hz | Max Vel: {self.max_vel}m/s")

        # Create a timer loop tracking our frequency parameter
        timer_period = 1.0 / self.frequency
        self.execution_timer = self.create_timer(timer_period, self.timer_execution_loop)

        # ==============================================================================
        # 3. DYNAMIC UPDATE REGISTRATION
        # ==============================================================================
        self.add_on_set_parameters_callback(self.parameter_modification_callback)

    def timer_execution_loop(self):
        """Standard processing loop running at the speed dictated by the parameter."""
        self.get_logger().info(f"[RUNNING] Processing logic in safety state: [{self.safety_mode}]")

    def parameter_modification_callback(self, parameter_list):
        """Triggers automatically whenever parameters are updated via CLI or Launch scripts."""
        result = SetParametersResult()
        result.successful = True  # Tell the system the change is allowed
        
        for param in parameter_list:
            if param.name == 'robot_safety_mode':
                self.safety_mode = param.value
                self.get_logger().warn(f"CRITICAL: Safety configuration changed to: {self.safety_mode}")
                
            elif param.name == 'execution_frequency':
                self.frequency = param.value
                # Dynamically alter the running timer parameters in memory without deleting the object
                new_period_ns = int((1.0 / self.frequency) * 1e9)
                self.execution_timer.timer_period_ns = new_period_ns
                self.get_logger().warn(f"SYSTEM: Execution timer frequency updated to {self.frequency}Hz")
                
            elif param.name == 'max_linear_velocity':
                # Add validation limits before accepting changes
                if param.value > 2.0:
                    self.get_logger().error(f"REJECTED: Speed value {param.value} exceeds maximum physical motor capability!")
                    result.successful = False
                    result.reason = "Velocity exceeds safety limit of 2.0 m/s"
                else:
                    self.max_vel = param.value
                    self.get_logger().info(f"SYSTEM: Updated linear velocity threshold to {self.max_vel}m/s")

        return result

def main(args=None):
    rclpy.init(args=args)
    node = ParamTuningNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
2. Update package.xml and setup.py
Ensure your node is executable and correctly mapped inside your Python package.

In package.xml, confirm you have rclpy mapped:

XML
<depend>rclpy</depend>
In setup.py, expose the node point entry mapping cleanly:

Python
    entry_points={
        'console_scripts': [
            'param_tuning_node = your_package.param_tuning_node:main',
        ],
    },
Interacting with Parameters via Terminal (CLI)
Once you build and compile your workspace (colcon build && source install/setup.bash), you can fully inspect and manipulate your parameters directly from the command line while your node runs.

1. Run the Node
Bash
ros2 run your_package param_tuning_node
2. List Active Parameters
Open a second terminal window and run the following to discover all declared parameters belonging to a node:

Bash
ros2 param list
Output:

Plaintext
/param_tuning_node:
  execution_frequency
  max_linear_velocity
  robot_safety_mode
  use_sim_time
3. Read an Active Parameter Value
To check the exact current assignment state of a specific key variable:

Bash
ros2 param get /param_tuning_node robot_safety_mode
Output:

Plaintext
String value is: standard
4. Dynamic Live Adjustment (The Magic Step)
To change a node parameter while the code execution loop is actively cycling inside your robot:

Bash
ros2 param set /param_tuning_node execution_frequency 4.0
Look back at your main running node window. The output log will instantly adapt, running your processing loop four times faster every single second without a restart!

If you try to inject an unsafe value that violates your validation conditions:

Bash
ros2 param set /param_tuning_node max_linear_velocity 5.2
The terminal will return a failure report, and your node will throw a rejected log flag keeping your system safe.

Loading Parameters via YAML Configuration Files
When running automated architectures or launch setups, passing continuous updates through raw terminals is inefficient. Instead, you drop configurations into standard .yaml resource sheets.

1. Create the Config File
Create a new directory and configuration sheet inside your package architecture (src/your_package/config/robot_params.yaml):

YAML
/param_tuning_node:
  ros__parameters:
    execution_frequency: 2.5
    robot_safety_mode: "emergency_override"
    max_linear_velocity: 1.2
CRITICAL SYNTAX NOTE: ROS 2 configuration parameters require a strict two-space indentation structure, a clear root namespace identifier (/param_tuning_node), and a dedicated tag label titled exactly ros__parameters: (with two consecutive underscores).

2. Boot up Using the Configuration File
To spin up your node while forcing it to read all its default parameters directly out of your custom parameters configuration sheet, use the --ros-args flag argument structure:

Bash
ros2 run your_package param_tuning_node --ros-args --params-file src/your_package/config/robot_params.yaml
The node will initialize with the frequency set to 2.5Hz and safety configuration automatically re-mapped to emergency_override.