import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class Follower(Node):

    def __init__(self):
        super().__init__('follower')

        self.sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.update_pose,
            10)

        self.pub = self.create_publisher(
            Twist,
            '/turtle2/cmd_vel',
            10)

    def update_pose(self, msg):
        cmd = Twist()

        # Simple proportional controller
        cmd.linear.x = 1.5 * msg.x
        cmd.angular.z = 4.0 * msg.theta

        self.pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = Follower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()