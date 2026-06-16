import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from rcl_interfaces.msg import SetParametersResult

class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('velocity_publisher')
        self.declare_parameter('velocity', 1.0)
        self.robot_speed = self.get_parameter('velocity').get_parameter_value().double_value

        self.publisher_ = self.create_publisher(Float32, 'velocity', 10)
        self.timer = self.create_timer(1.0, self.publish_velocity)
        self.add_on_set_parameters_callback(self.parameter_callback)

    def publish_velocity(self): 
        velocity = self.get_parameter('velocity').get_parameter_value().double_value or 0.0
        msg = Float32()
        msg.data = velocity
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published velocity: {velocity}')

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'velocity' and param.type_ == rclpy.Parameter.Type.DOUBLE:
                if 0.0 <= param.value <= 10.0:
                    self.robot_speed = param.value
                    self.get_logger().info(f'Updated velocity to: {self.robot_speed}')
                else:
                    self.get_logger().info('Skipping update: velocity must be between 0.0 and 10.0')
                return SetParametersResult(successful=True)
        self.get_logger().error('Invalid parameter type or name')
        return SetParametersResult(successful=False, reason='Invalid parameter type or name')

def main(args=None):
    rclpy.init(args=args)
    velocity_publisher = VelocityPublisher()
    rclpy.spin(velocity_publisher)
    velocity_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':    
    main()