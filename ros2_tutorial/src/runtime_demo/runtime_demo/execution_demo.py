import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor, MultiThreadedExecutor
import time
class RuntimeDemoNode(Node):
    def __init__(self):
        super().__init__('runtime_demo_node')
        self.get_logger().info('Runtime Demo Node has started.')
        self.timer1 = self.create_timer(1.0, self.timer_callback_1)
        self.timer2 = self.create_timer(2.0, self.timer_callback_2)
    
    def timer_callback_1(self):
        self.get_logger().info('Timer 1: This message is printed every 1 second.')
        time.sleep(5)

    def timer_callback_2(self):
        self.get_logger().info('Timer 2: This message is printed every 2 seconds.')


def main(args=None):
    rclpy.init(args=args)
    runtime_demo_node = RuntimeDemoNode()
    executor = MultiThreadedExecutor()
    executor.add_node(runtime_demo_node)
    executor.spin()
    runtime_demo_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()