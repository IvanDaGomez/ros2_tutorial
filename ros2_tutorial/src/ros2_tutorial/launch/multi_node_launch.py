from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import GroupAction
from launch.conditions import IfCondition
def generate_launch_description():
    robot_speed_arg = DeclareLaunchArgument(
        'robot_speed',
        default_value='1.0',
        description='Speed of the robot'
    )
    robot_speed = LaunchConfiguration('robot_speed')

    enable_callback_arg = DeclareLaunchArgument(
        'enable_callback',
        default_value='true',
        description='Enable parameter callback'
    )
    enable_callback = LaunchConfiguration('enable_callback')
    return LaunchDescription([
        robot_speed_arg,
        enable_callback_arg,
        GroupAction([
        Node(
            package='ros2_tutorial',
            executable='service_node',
            namespace='robot1',
            condition=IfCondition(enable_callback),
            name='service_node',
            output='screen'
        ),
        Node(
            package='ros2_tutorial',
            executable='client_service_node',
            namespace='robot1',
            name='client_service_node'
        ),
        Node(
            package='ros2_tutorial',
            executable='action_service_node',
            namespace='robot1',
            name='action_service_node'
        ),
        ]),
        Node(
            package='ros2_tutorial',
            executable='action_client_node',
            namespace='robot1',
            name='action_client_node'
        ),
        Node(
            package='ros2_tutorial',
            executable='parameter_example',
            namespace='robot1',
            name='parameter_example',
            parameters=[{'robot_speed': robot_speed}]
        ),
        Node(
            package='ros2_tutorial',
            namespace='robot1',
            executable='parameter_callback',
            name='parameter_callback'
        )
    ])
    # ros2 launch ros2_tutorial multi_node_launch.py
    # ros2 launch ros2_tutorial multi_node_launch.py robot_speed:=2.5