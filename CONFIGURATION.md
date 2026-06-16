# Masterclass Topic: Managing ROS 2 Node Parameter Files (YAML)

When building production-grade autonomous systems, you should never hardcode parameters (like maximum velocities, sensor topic names, or PID gains) directly inside your source files. If you do, you have to modify your code and recompile your package every single time you change a single value.

Instead, ROS 2 utilizes YAML configuration files to feed parameters directly into your nodes at runtime, allowing you to tweak hardware configurations instantly without changing a single line of code.

## 🛠️ Section 1: The YAML File Structure

For a ROS 2 node to accept an external configuration file, the YAML data must match a strict structural schema.

Create a file named `config.yaml` inside your package layout: `src/ros2_first_project/config/config.yaml`.

```yaml
/velocity_publisher:     # <--- Node Name Namespace
  ros__parameters:       # <--- Parameter Indicator (Double Underscore!)
    max_linear_speed: 2.5
    loop_rate_hz: 10
    debug_mode: true
```

The Rules of ROS 2 YAML Files:

- The Node Name (`/velocity_publisher`): The very first line must match the exact name assigned to your node when it is run. If the names do not align perfectly, the node will completely ignore the parameters.
- The ROS Parameter Tag (`ros__parameters`): This is a hardcoded keyword that tells the ROS 2 parameters engine to parse the nested keys underneath it. Note the double underscore (`__`)—this is a frequent syntax trap that will crash your node initialization if typed as a single underscore.

## 🏗️ Section 2: Reading Parameters in the Python Node

To make use of these configuration files, your Python script must explicitly declare the parameters in its constructor (`__init__`) before it can read them.

Here is the clean boilerplate configuration for `velocity_publisher.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class VelocityPublisher(Node):

    def __init__(self):
        super().__init__('velocity_publisher') # <--- Must match the YAML name!

        # 1. Declare the parameters with safe baseline defaults
        self.declare_parameter('max_linear_speed', 1.0)
        self.declare_parameter('loop_rate_hz', 5)
        self.declare_parameter('debug_mode', False)

        # 2. Fetch the values (overwritten by the YAML file automatically if provided)
        self.max_speed = self.get_parameter('max_linear_speed').value
        self.rate = self.get_parameter('loop_rate_hz').value
        self.is_debug = self.get_parameter('debug_mode').value

        self.get_logger().info(f"Node initialized with max_speed: {self.max_speed} at {self.rate}Hz")

def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

⚠️ **Critical Package Architecture Check**

Because ROS 2 executes files out of the `install/` directory and not your active development `src/` folder, your build tools need to know how to export your configuration folder.

Open your package's `setup.py` file and verify that your `data_files` array explicitly copies your configuration pathway:

```python
import os
from glob import glob

# Inside your setup() block:
data_files=[
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    
    # CRITICAL: Maps and copies your config directory so it exists in the install/ share space
    (os.path.join('share', package_name, 'config'), glob('config/*.yaml')), 
]
```

## 🚀 Running Nodes Manually with Config Files

If you want to run your node directly from the command line using standard execution tools while passing your configuration file manually, use the `--ros-args` and `--params-file` flags:

```bash
ros2 run ros2_first_project velocity_publisher --ros-args --params-file src/ros2_first_project/config/config.yaml
```