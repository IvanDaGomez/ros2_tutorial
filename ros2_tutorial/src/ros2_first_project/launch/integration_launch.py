from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    robot_speed_arg = DeclareLaunchArgument(
        'robot_speed',
        default_value='1.0',
        description='Speed of the robot'
    )
    robot_speed = LaunchConfiguration('robot_speed')

    return LaunchDescription([
        robot_speed_arg,
        Node(
            package='ros2_first_project',
            executable='velocity_publisher',
            name='velocity_publisher_node',
            output='screen',
            parameters=[{'velocity': robot_speed}]
        )
    ])