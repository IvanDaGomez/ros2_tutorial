# ROS2 Tutorial

## How to create an action

1. Create an interface package inside the `src` folder of the workspace.

```bash
cd ~/Documents/ros2_tutorial/src
ros2 pkg create --build-type ament_cmake ros2_tutorial_interfaces
Create an action folder and file inside the custom interface package.

Bash
mkdir -p ros2_tutorial_interfaces/action
touch ros2_tutorial_interfaces/action/Fibonacci.action
Define the action interface in the Fibonacci.action file.

Plaintext
# Goal definition
int32 order
---
# Result definition
int32[] sequence
---
# Feedback definition
int32[] partial_sequence
Configure the interface package files to compile the action bindings correctly.

Inside ros2_tutorial_interfaces/CMakeLists.txt, ensure it includes the generator macro before the ament_package() seal:

CMake
cmake_minimum_required(VERSION 3.8)
project(ros2_tutorial_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find Generation Dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate Action Interfaces
rosidl_generate_interfaces(${PROJECT_NAME}
  "action/Fibonacci.action"
)

# Export Dependencies for Runtime Use
ament_export_dependencies(rosidl_default_runtime)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
Inside ros2_tutorial_interfaces/package.xml, include the interface package group strictly wrapped inside the <export> element:

XML
<?xml version="1.0"?>
<?xml-model href="[http://download.ros.org/schema/package_format3.xsd](http://download.ros.org/schema/package_format3.xsd)" schematypens="[http://www.w3.org/2001/XMLSchema](http://www.w3.org/2001/XMLSchema)"?>
<package format="3">
  <name>ros2_tutorial_interfaces</name>
  <version>0.0.0</version>
  <description>Custom action interface package</description>
  <maintainer email="ubuntu@todo.todo">ubuntu</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>rosidl_default_generators</buildtool_depend>

  <exec_depend>rosidl_default_runtime</exec_depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
    <member_of_group>rosidl_interface_packages</member_of_group>
  </export>
</package>
Build the interface package first to generate your custom dependencies.

Bash
cd ~/Documents/ros2_tutorial
rm -rf build/ros2_tutorial_interfaces install/ros2_tutorial_interfaces
colcon build --packages-select ros2_tutorial_interfaces
Create a separate python package for the action nodes (if not already created).

Bash
cd ~/Documents/ros2_tutorial/src
ros2 pkg create --build-type ament_python ros2_tutorial
Update your processing configuration manifest files for your python nodes.

Inside ros2_tutorial/package.xml, declare the custom interface package dependency (Do NOT add any interface group or export tags here):

XML
<?xml version="1.0"?>
<?xml-model href="[http://download.ros.org/schema/package_format3.xsd](http://download.ros.org/schema/package_format3.xsd)" schematypens="[http://www.w3.org/2001/XMLSchema](http://www.w3.org/2001/XMLSchema)"?>
<package format="3">
  <name>ros2_tutorial</name>
  <version>0.0.0</version>
  <description>Python application nodes package</description>
  <maintainer email="ubuntu@todo.todo">ubuntu</maintainer>
  <license>Apache-2.0</license>

  <depend>rclpy</depend>
  <depend>ros2_tutorial_interfaces</depend>
  <depend>action_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
Create the execution scripts inside your package source directory.

Bash
cd ~/Documents/ros2_tutorial/src/ros2_tutorial/ros2_tutorial
touch action_server_node.py action_client_node.py
chmod +x action_server_node.py action_client_node.py
Implement clean execution logic blocks without indentation nesting traps.

Python
# action_server_node.py
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from ros2_tutorial_interfaces.action import Fibonacci

class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)
        self.get_logger().info("Action Server has been initialized.")

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        order = goal_handle.request.order
        sequence = [0, 1]
        
        for i in range(2, order + 1):
            sequence.append(sequence[i - 1] + sequence[i - 2])
            feedback_msg = Fibonacci.Feedback()
            feedback_msg.partial_sequence = sequence[:i + 1]
            goal_handle.publish_feedback(feedback_msg)
            
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = sequence[:order + 1]
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = FibonacciActionServer()
    try:
        rclpy.spin(action_server)
    except KeyboardInterrupt:
        pass
    finally:
        action_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
Python
# action_client_node.py
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from ros2_tutorial_interfaces.action import Fibonacci

class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')
        self.get_logger().info("Action Client has been initialized.")

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')

def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    action_client.send_goal(10)
    try:
        rclpy.spin(action_client)
    except KeyboardInterrupt:
        pass
    finally:
        action_client.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
Expose the execution nodes in your package's setup.py layout.

Python
    entry_points={
        'console_scripts': [
            'action_server_node = ros2_tutorial.action_server_node:main',
            'action_client_node = ros2_tutorial.action_client_node:main',
        ],
    },
Compile the workspace from a clean state and launch.

Bash
cd ~/Documents/ros2_tutorial
rm -rf build/ install/ log/
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
ros2 run ros2_tutorial action_client_node