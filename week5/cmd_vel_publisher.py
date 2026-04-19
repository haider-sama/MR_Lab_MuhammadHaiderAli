import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelPublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.moving = False  # Start with zero, alternate each callback
        self.get_logger().info('cmd_vel publisher started')

    def timer_callback(self):
        msg = Twist()
        if self.moving:
            msg.linear.x = 0.2  # Forward at 0.2 m/s
            self.get_logger().info('Publishing: FORWARD (linear.x = 0.2)')
        else:
            msg.linear.x = 0.0  # Stop
            self.get_logger().info('Publishing: STOP (linear.x = 0.0)')
        self.publisher_.publish(msg)
        self.moving = not self.moving  # Toggle state


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()