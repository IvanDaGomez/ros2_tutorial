import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
    def send_request(self, a, b):
        req = AddTwoInts.Request()
        req.a = a
        req.b = b
        self.future = self.cli.call_async(req)
def main(args=None):
    rclpy.init(args=args)
    add_two_ints_client = AddTwoIntsClient()
    add_two_ints_client.send_request(5, 3)
    while rclpy.ok():
        rclpy.spin_once(add_two_ints_client)
        if add_two_ints_client.future.done():
            try:
                response = add_two_ints_client.future.result()
            except Exception as e:
                add_two_ints_client.get_logger().info(f'Service call failed: {e}')
            else:
                add_two_ints_client.get_logger().info(f'Result of add_two_ints: {response.sum}')
            break
    add_two_ints_client.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()