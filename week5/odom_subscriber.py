import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_subscriber')
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        self.get_logger().info('Odom subscriber started, listening to /odom...')

    def odom_callback(self, msg):
        pos = msg.pose.pose.position
        ori = msg.pose.pose.orientation
        lin = msg.twist.twist.linear
        ang = msg.twist.twist.angular

        self.get_logger().info(
            f'\n--- Odometry Data ---\n'
            f'Position    -> x: {pos.x:.4f}, y: {pos.y:.4f}, z: {pos.z:.4f}\n'
            f'Orientation -> x: {ori.x:.4f}, y: {ori.y:.4f}, z: {ori.z:.4f}, w: {ori.w:.4f}\n'
            f'Lin Velocity-> x: {lin.x:.4f}, y: {lin.y:.4f}, z: {lin.z:.4f}\n'
            f'Ang Velocity-> x: {ang.x:.4f}, y: {ang.y:.4f}, z: {ang.z:.4f}\n'
        )


def main(args=None):
    rclpy.init(args=args)
    node = OdomSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()