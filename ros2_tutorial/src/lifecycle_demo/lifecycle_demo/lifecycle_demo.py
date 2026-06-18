import rclpy
from rclpy.lifecycle import LifecycleNode, State, TransitionCallbackReturn
from std_msgs.msg import String

class LifecycleDemoNode(LifecycleNode):
    def __init__(self):
        super().__init__('lifecycle_demo_node')
        self.publisher = None
        self.timer = None
        self.count = 0


    def on_configure(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Configuring the node...')
        self.publisher = self.create_lifecycle_publisher(String, 'lifecycle_demo_topic', 10)
        # Perform any necessary configuration here
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Activating the node...')
        self.timer = self.create_timer(1.0, self.publish_message)
        # Start publishing messages or perform any necessary activation steps here
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Deactivating the node...')
        if self.timer:
            self.destroy_timer(self.timer)
        # Stop publishing messages or perform any necessary deactivation steps here
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Cleaning up the node...')
        if self.publisher:
            self.destroy_publisher(self.publisher)
        if self.timer:
            self.destroy_timer(self.timer)
        # Clean up resources or perform any necessary cleanup steps here
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info('Shutting down the node...')
        # Perform any necessary shutdown steps here
        return TransitionCallbackReturn.SUCCESS

    def publish_message(self):
        msg = String()
        msg.data = f'Hello, this is message number {self.count}'
        if self.publisher:
            self.publisher.publish(msg)
            self.get_logger().info(f'Published: {msg.data}')
            self.count += 1

def main(args=None):
    rclpy.init(args=args)
    lifecycle_node = LifecycleDemoNode()
    rclpy.spin(lifecycle_node)
    lifecycle_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()