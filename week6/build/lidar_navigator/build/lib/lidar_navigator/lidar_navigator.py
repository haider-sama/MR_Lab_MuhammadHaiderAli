import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

class LidarNavigator(Node):
    def __init__(self):
        super().__init__('lidar_navigator')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # TODO: Define thresholds
        self.front_threshold = 0.35   # metres — stop if obstacle closer than this
        self.side_threshold  = 0.25   # metres — used for wall-follow clearance

    def scan_callback(self, msg):
        ranges = np.array(msg.ranges)

        # -----------------------------
        # TODO 1: Clean data (remove inf/nan)
        # -----------------------------
        ranges = np.where(np.isfinite(ranges), ranges, 3.5)

        # -----------------------------
        # TODO 2: Define regions
        # (TurtleBot3 burger: 360 rays, index 0 = front)
        # Front  : -30° to +30°  → indices 0-30 and 330-359
        # Left   : 60° to 120°   → indices 60-120
        # Right  : 240° to 300°  → indices 240-300
        # -----------------------------
        front = np.concatenate((ranges[0:31], ranges[330:360]))
        left  = ranges[60:121]
        right = ranges[240:301]

        # Compute minimum distance
        front_dist = float(np.min(front))
        left_dist  = float(np.min(left))
        right_dist = float(np.min(right))

        # Debug output
        self.get_logger().info(f"Front: {front_dist:.2f}  Left: {left_dist:.2f}  Right: {right_dist:.2f}")

        twist = Twist()

        # -----------------------------
        # TODO 3: Obstacle logic
        # -----------------------------
        if front_dist < self.front_threshold:   # obstacle in front

            # -------------------------
            # TODO 4: Turn direction
            # -------------------------
            if left_dist > right_dist:          # left clearer
                twist.angular.z =  0.5          # turn left  (positive = CCW)
            else:
                twist.angular.z = -0.5          # turn right (negative = CW)

            twist.linear.x = 0.0               # stop forward motion while turning

        else:
            # -------------------------
            # TODO 5: Forward motion
            # -------------------------
            twist.linear.x  = 0.15             # move forward
            twist.angular.z = 0.0              # straight

        self.publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = LidarNavigator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()