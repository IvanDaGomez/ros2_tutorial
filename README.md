# ROS2 Tutorial

## How to create an action

1. Create an interface package inside the src folder of the workspace.

```bash
ros2 pkg create --build-type ament_cmake ros2_tutorial_interfaces
```
2. Create an action file inside the action folder of the interface package.

```bash
mkdir -p src/ros2_tutorial_interfaces/action
touch src/ros2_tutorial_interfaces/action/Fibonacci.action
```
3. Define the action interface in the Fibonacci.action file.
```plaintext
# Goal definition
int32 order
---
# Result definition
int32[] sequence
---
# Feedback definition
int32[] partial_sequence
```
4. Build the interface package to generate the necessary code for the action.
```bash
colcon build --packages-select ros2_tutorial_interfaces
```
5. Edit CMakeLists.txt and package.xml to include the new action interface.
Inside CMakeLists.txt, add the following lines:
```cmake
find_package(rosidl_default_generators REQUIRED)


amend_package_xml()

if(NOT ros2_tutorial_interfaces_EXPORTED_GROUPS)
  list(APPEND ros2_tutorial_interfaces_EXPORTED_GROUPS "rosidl_interface_packages")
endif()
rosidl_generate_interfaces(${PROJECT_NAME}
  "action/Fibonacci.action"
)
ament_export_dependencies(rosidl_default_runtime)

```
Inside both package.xml files, add the following lines:
```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>

<export>
  <member_of_group>rosidl_interface_packages</member_of_group>
</export>
```
6. Create a new package for the action server and client. (If not already created)
```bash
ros2 pkg create --build-type ament_python ros2_tutorial
```
7. Include the action interface in the package.xml of the action server and client package.
```xml
<depend>ros2_tutorial_interfaces</depend>
```
8. Create the action server and client nodes in the ros2_tutorial package.
Create files for the action server and client nodes:
```bash
touch src/ros2_tutorial/action_server.py
touch src/ros2_tutorial/action_client.py
```
9. Implement the action server and client logic in the respective files.
10. Edit the setup.py file to include the new action server and client nodes in the entry points.
(Samples of action server and client)
```python
# action_server.py
import rclpy
from rclpy.node import Node
from ros2_tutorial_interfaces.action import Fibonacci
from rclpy.action import ActionServer

class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

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
    rclpy.spin(action_server)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
```
```python
# action_client.py
import rclpy
from rclpy.node import Node
from ros2_tutorial_interfaces.action import Fibonacci
from rclpy.action import ActionClient

class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

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
    rclpy.spin(action_client)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
```
