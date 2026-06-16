import rclpy
from rclpy.node import Node
from ros2_tutorial_interfaces.action import Fibonacci
from rclpy.action import ActionServer
import time
class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        order = goal_handle.request.order
        sequence = [0, 1]
        for i in range(2, order + 1):
            sequence.append(sequence[i - 1] + sequence[i - 2])
            feedback_msg = Fibonacci.Feedback()
            feedback_msg.partial_sequence = sequence[:i + 1]
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Published feedback: {feedback_msg.partial_sequence}')
            time.sleep(1) 
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = sequence[:order + 1]
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = FibonacciActionServer()
    rclpy.spin(action_server)
    rclpy.shutdown()
if __name__ == '__main__':
    main()