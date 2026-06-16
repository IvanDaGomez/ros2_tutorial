from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory
def generate_launch_description():
    config_file = os.path.join(get_package_share_directory('ros2_first_project'), 'config', 'config.yaml')
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
            name='velocity_publisher',
            output='screen',
            parameters=[config_file]
        )
    ])