import rclpy
from rclpy.node import Node
import os

class SimpleNode(Node):

    def __init__(self):
        super().__init__('simple_node')

        # Task 1 message
        self.get_logger().info('Welcome to Mobile Robotics Lab')

        # Task 2: Counter logic
        counter_file = os.path.join(
            os.path.dirname(__file__),
            'counter.txt'
        )

        count = 0

        if os.path.exists(counter_file):
            with open(counter_file, 'r') as f:
                count = int(f.read().strip())

        count += 1

        with open(counter_file, 'w') as f:
            f.write(str(count))

        self.get_logger().info(f'Run count: {count}')

        # Task 3: Parameter
        self.declare_parameter('student_name', '')

        name = self.get_parameter('student_name').value

        if name:
            self.get_logger().info(f'Student Name: {name}')
        else:
            self.get_logger().info('student_name not set')


def main(args=None):
    rclpy.init(args=args)
    node = SimpleNode()
    rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()