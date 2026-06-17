import rclpy
from rclpy.node import Node, ReentrantCallbackGroup
from geometry_msgs.msg import Twist
import time
from rclpy.executors import MultiThreadedExecutor
import threading

class TurtleControlNode(Node):
    def __init__(self):
        super().__init__('turtle_control_node')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.reentrant_group = ReentrantCallbackGroup()
        self.timer = self.create_timer(1.0, self.publish_velocity, callback_group=self.reentrant_group)
        self.heavy_timer = self.create_timer(5.0, self.heavy_computation, callback_group=self.reentrant_group)

    def publish_velocity(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.publisher_.publish(msg)
        time.sleep(0.01)
        self.get_logger().info(f'Published velocity command: linear.x={msg.linear.x}, angular.z={msg.angular.z}')

    def heavy_computation(self):
        self.get_logger().info('Starting heavy computation...')
        time.sleep(5)
        self.get_logger().info('Heavy computation completed.')

def main(args=None):
    rclpy.init(args=args)
    turtle_control_node = TurtleControlNode()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(turtle_control_node)
    executor.spin()
    turtle_control_node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()