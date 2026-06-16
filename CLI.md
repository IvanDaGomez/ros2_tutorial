# ROS2 Command Line Interface (CLI) deep dive

## Node Management
ros2 node list: List all active nodes in the ROS2 system.
ros2 node info /node_name: Get detailed information about a specific node, including its publishers, subscribers, services, actions, and parameters.

## Topic Management
ros2 topic list: List all active topics.
ros2 topic type /topic_name: Get the message type of a specific topic.
ros2 topic info /topic_name: Get detailed information about a specific topic, including its publishers and subscribers.
ros2 topic echo /topic_name: Display the messages being published on a specific topic in real-time.
ros2 topic pub /topic_name message_type "data": Publish a message to a specific topic from the command line.

## Service Management
ros2 service list: List all active services.
ros2 service call /service_name: Call a specific service with the required request parameters.
ros2 service type /service_name: Get the request and response message types of a specific service.
ros2 service info /service_name: Get detailed information about a specific service, including its providers and clients.

## Action Management
ros2 action list: List all active actions.
ros2 action send_goal /action_name: Send a goal to a specific action server and monitor its progress.
ros2 action type /action_name: Get the goal, result, and feedback message types of a specific action.
ros2 action info /action_name: Get detailed information about a specific action, including its servers and clients.
ros2 action cancel /action_name: Cancel an active goal for a specific action.
ros2 action list /action_name: List all active goals for a specific action.
ros2 action send_goal /action_name --feedback: Send a goal to a specific action server and display feedback in real-time.

## Parameter Management
ros2 param list: List all parameters for a specific node.
ros2 param get /node_name parameter_name: Get the value of a specific parameter for a node.
ros2 param set /node_name parameter_name value: Set the value of a specific parameter for a node.
ros2 param describe /node_name parameter_name: Get detailed information about a specific parameter, including its type, default value, and constraints.
ros2 param dump /node_name: Dump all parameters of a node in YAML format for easy inspection and modification.
ros2 param load /node_name parameters.yaml: Load parameters from a YAML file into a specific node.
ros2 param set /node_name parameter_name value --type type: Set the value of a specific parameter with an explicit type, useful for complex types like lists or dictionaries.

## Launch File Management
ros2 launch package_name launch_file.launch.py: Launch a ROS2 application using a specified launch file.
ros2 launch --show-args package_name launch_file.launch.py: Display the arguments that can be passed to a launch file.
ros2 launch --show-logs package_name launch_file.launch.py: Display the log output from a launch file in real-time.
ros2 launch package_name launch_file.launch.py arg_name:=value: Pass a specific argument to a launch file at runtime.

## Interface Management
ros2 interface list: List all available message, service, and action types.
ros2 interface show message_type: Display the structure of a specific message type.
ros2 interface show service_type: Display the request and response structure of a specific service type.
ros2 interface show action_type: Display the goal, result, and feedback structure of a specific action type.

## Additional CLI Tools
ros2 bag record /topic_name: Record messages from a specific topic into a ROS2 bag file for later analysis.
ros2 bag play bag_file: Play back messages from a ROS2 bag file.
ros2 lifecycle set /node_name state: Transition a node through its lifecycle states (e.g., configure, activate, deactivate, cleanup, shutdown).
ros2 lifecycle get /node_name: Get the current lifecycle state of a node.
