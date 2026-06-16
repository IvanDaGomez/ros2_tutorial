ROS 2 Launch Files: Complete Tutorial
Introduction

ROS 2 launch files provide a way to start, configure, and manage one or more nodes from a single command. They are the preferred mechanism for launching complete robotic systems because they allow you to:

Start multiple nodes simultaneously
Configure parameters
Set namespaces
Remap topics and services
Conditionally launch components
Group related actions
Include other launch files
Execute arbitrary processes
Manage complex robot deployments

Without launch files, a robot consisting of dozens of nodes would require many terminal windows and manual configuration. Launch files automate this process and make systems reproducible.

Basic Structure

A Python launch file typically follows this structure:

from launch import LaunchDescription

def generate_launch_description():
    return LaunchDescription([
        # Actions go here
    ])

The generate_launch_description() function is the entry point of every launch file. It returns a LaunchDescription object containing a list of actions that should be executed.

Actions

Everything inside a launch file is an action.

Examples include:

Launching a node
Declaring arguments
Setting parameters
Including another launch file
Running an external process
Creating groups
Applying conditions

Example:

return LaunchDescription([
    action_1,
    action_2,
    action_3
])

Actions are executed by the launch system when the file starts.

Launching Nodes

The most common action is launching a node.

from launch_ros.actions import Node

Node(
    package='my_package',
    executable='my_node'
)

This is equivalent to:

ros2 run my_package my_node
Common Node Arguments
Name
Node(
    package='my_package',
    executable='my_node',
    name='controller'
)

Node name becomes:

/controller
Namespace
Node(
    package='my_package',
    executable='my_node',
    namespace='robot1'
)

Node path becomes:

/robot1/my_node

Namespaces are especially useful in multi-robot systems.

Output
Node(
    package='my_package',
    executable='my_node',
    output='screen'
)

Displays logs directly in the terminal.

Common values:

output='screen'
output='log'
Launch Arguments

Launch arguments allow users to customize launch behavior at runtime.

from launch.actions import DeclareLaunchArgument

DeclareLaunchArgument(
    'robot_speed',
    default_value='1.0',
    description='Robot speed'
)
Running With Arguments

Default:

ros2 launch my_package robot.launch.py

Custom value:

ros2 launch my_package robot.launch.py robot_speed:=2.5
LaunchConfiguration

Launch arguments become useful through LaunchConfiguration.

from launch.substitutions import LaunchConfiguration

robot_speed = LaunchConfiguration('robot_speed')

This creates a runtime reference to the launch argument.

Passing Parameters

Parameters can be passed directly to nodes.

Node(
    package='my_package',
    executable='controller',
    parameters=[
        {'robot_speed': robot_speed}
    ]
)

The node receives:

robot_speed = 2.5

if launched with:

ros2 launch my_package robot.launch.py robot_speed:=2.5
Parameter Files

Instead of individual parameters, entire YAML files can be loaded.

Example YAML:

controller:
  ros__parameters:
    robot_speed: 2.5
    max_acceleration: 1.0

Launch file:

Node(
    package='my_package',
    executable='controller',
    parameters=['config/controller.yaml']
)

This is the preferred method for larger projects.

Parameter Callbacks

A node may react whenever a parameter changes.

Example concept:

node.set_on_parameters_set_callback(
    parameter_callback
)

This callback executes before the parameter is applied.

Common uses:

Validation
Safety checks
Dynamic reconfiguration
Preventing invalid values

Example:

speed > 0

Allowed.

speed < 0

Rejected.

Dynamic Parameter Updates

Parameters can be modified while nodes are running.

ros2 param set /controller robot_speed 3.0

The node immediately receives the update.

Combined with callbacks, this enables runtime tuning without restarting nodes.

Conditions

Conditions determine whether an action executes.

Example:

from launch.conditions import IfCondition

Node(
    package='my_package',
    executable='debug_node',
    condition=IfCondition(debug_mode)
)

If:

debug_mode = true

the node launches.

Otherwise it is skipped.

Example Argument-Controlled Condition

Argument:

DeclareLaunchArgument(
    'enable_camera',
    default_value='true'
)

Configuration:

enable_camera = LaunchConfiguration('enable_camera')

Conditional node:

Node(
    package='camera_pkg',
    executable='camera_node',
    condition=IfCondition(enable_camera)
)

Usage:

ros2 launch robot.launch.py enable_camera:=false

Camera node is not launched.

Groups

Groups allow actions to be organized together.

from launch.actions import GroupAction

GroupAction([
    action1,
    action2,
    action3
])
Why Use Groups?

Groups can:

Share namespaces
Share remappings
Share parameters
Organize related nodes

Example:

GroupAction([
    Node(...),
    Node(...),
    Node(...)
])

All nodes belong to the same logical subsystem.

Namespaces and Multi-Robot Systems

Suppose two robots use identical nodes.

Without namespaces:

/controller
/laser
/odom

Conflicts occur.

Using namespaces:

/robot1/controller
/robot1/laser

/robot2/controller
/robot2/laser

Both robots can operate simultaneously.

Remappings

Remappings redirect topics, services, or actions.

Node expects:

/cmd_vel

Launch file:

Node(
    package='my_package',
    executable='controller',
    remappings=[
        ('cmd_vel', 'robot1/cmd_vel')
    ]
)

The node now uses:

/robot1/cmd_vel

without changing source code.

Services

Services implement request-response communication.

Typical architecture:

Client ----> Service Server
       Request
       Response

Launch files simply start the participating nodes.

Example:

Node(
    package='my_package',
    executable='service_server'
)

Node(
    package='my_package',
    executable='service_client'
)

The launch system does not create services—it only launches the nodes that provide them.

Actions

Actions are used for long-running tasks.

Examples:

Navigation
Trajectory execution
Manipulation
Docking

Architecture:

Action Client
      |
      v
Action Server

Communication includes:

Goal
Feedback
Result

Launch file:

Node(
    package='my_package',
    executable='action_server'
)

Node(
    package='my_package',
    executable='action_client'
)

Again, the launch system only starts the nodes.

Including Other Launch Files

Large systems often split launch files.

Main launch:

from launch.actions import IncludeLaunchDescription
IncludeLaunchDescription(...)

Benefits:

Better organization
Reusable subsystems
Easier maintenance

Typical structure:

robot.launch.py
├── sensors.launch.py
├── navigation.launch.py
└── perception.launch.py
Executing External Processes

Launch files can execute arbitrary commands.

from launch.actions import ExecuteProcess

Example:

ExecuteProcess(
    cmd=['echo', 'Robot started']
)

Useful for:

Scripts
Simulators
External tools
Logging utilities
Event Handlers

Launch can react to events.

Examples:

Node starts
Node exits
Process crashes

Concept:

RegisterEventHandler(...)

Common use:

Start Node B after Node A exits

or

Restart a crashed component
Lifecycle Nodes

ROS 2 supports managed nodes with states:

Unconfigured
Inactive
Active
Finalized

Launch files can automate state transitions.

Useful for:

Safety-critical systems
Industrial robotics
Complex startup sequences
Substitutions

Substitutions generate values dynamically.

Examples:

LaunchConfiguration()
EnvironmentVariable()
PythonExpression()
TextSubstitution()

Example:

LaunchConfiguration('robot_name')

The value is resolved at launch time.

Common Launch Commands

Launch a file:

ros2 launch my_package robot.launch.py

Pass arguments:

ros2 launch my_package robot.launch.py speed:=2.0

Show available arguments:

ros2 launch my_package robot.launch.py --show-args

Print launch description:

ros2 launch my_package robot.launch.py --print-description
Best Practices
Use Launch Arguments

Avoid hardcoded values.

Good:

LaunchConfiguration('speed')

Bad:

speed = 2.5
Use YAML for Large Parameter Sets

Good:

parameters=['config/params.yaml']

Bad:

parameters=[
    {'a': 1},
    {'b': 2},
    {'c': 3},
    ...
]
Group Related Nodes
GroupAction([
    camera_node,
    image_processor,
    detector
])

Improves readability.

Use Namespaces Early

Even if your project currently has one robot.

Future expansion becomes easier.

Split Large Launch Files

Instead of:

1000-line launch file

Prefer:

main.launch.py
navigation.launch.py
perception.launch.py
control.launch.py
Typical Real-World Robot Structure
robot.launch.py
│
├── sensors.launch.py
│   ├── camera_node
│   ├── lidar_node
│   └── imu_node
│
├── localization.launch.py
│   ├── ekf_node
│   └── map_server
│
├── navigation.launch.py
│   ├── planner
│   ├── controller
│   └── recovery_server
│
└── control.launch.py
    ├── motor_controller
    ├── action_server
    └── service_server

This modular approach scales from small educational robots to large industrial systems.

Summary

Launch files are the orchestration layer of ROS 2. They allow you to:

Launch multiple nodes
Configure parameters
Use launch arguments
Dynamically substitute values
Group actions
Apply conditional execution
Manage namespaces
Remap interfaces
Include other launch files
Execute external processes
Handle events
Support services and actions
Build large, maintainable robotic systems

A well-designed launch system is often the difference between a robot that is easy to deploy and maintain and one that becomes difficult to manage as it grows.