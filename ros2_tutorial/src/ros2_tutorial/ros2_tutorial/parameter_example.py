import rclpy
from rclpy.node import Node

class ParameterExampleNode(Node):

    def __init__(self):
        super().__init__('parameter_example_node')
        self.declare_parameter('robot_speed', 1)
        self.get_logger().info(f'Parameter {self.get_parameter("robot_speed").name} declared with default value: {self.get_parameter("robot_speed").value}')
        parameter = self.get_parameter('robot_speed')
        self.get_logger().info(f'Current value of parameter {parameter.name}: {parameter.value}')
        robot_speed = parameter.value
        self.get_logger().info(f'Robot speed is set to: {robot_speed}')
def main(args=None):
    rclpy.init(args=args)
    parameter_example_node = ParameterExampleNode()
    rclpy.spin(parameter_example_node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()