import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
class ParameterCallbackExampleNode(Node):
    def __init__(self):
        super().__init__('parameter_callback_example_node')
        self.declare_parameter('example_parameter', 0.0)
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'example_parameter':
                if param.type_ == Parameter.Type.DOUBLE and (5.0 > param.value > 0.0):
                    self.get_logger().info(f'Parameter {param.name} set to {param.value}')
                    return SetParametersResult(successful=True)
                else:
                    self.get_logger().warn(f'Parameter {param.name} must be a positive double less than 5.0')
                    return SetParametersResult(successful=False, reason='Invalid type')
        return SetParametersResult()

def main(args=None):
    rclpy.init(args=args)
    parameter_callback_example_node = ParameterCallbackExampleNode()
    rclpy.spin(parameter_callback_example_node)
    parameter_callback_example_node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()