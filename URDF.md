xacro simple_robot.xacro > simple_robot.urdf
ros2 launch ros_gz_sim gz_sim.launch.py
sudo apt install ros-jazzy-xacro
ros2 run robot_state_publisher robot_state_publisher <filename.urdf>
ros2 run joint_state_publisher joint_state_publisher
sudo apt install ros-jazzy-tf2-tools
ros2 run tf2_tools view_frames
evince frames.pdf
ros2 run tf2_ros tf2_echo base_link left_wheel