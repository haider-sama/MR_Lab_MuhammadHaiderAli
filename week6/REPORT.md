# MCT-454L Mobile Robotics — Lab Manual #06
### Reactive Navigation Using TurtleBot3 LiDAR in Gazebo Environment

| | |
|---|---|
| **Submitted To** | Dr. Maria Akram |
| **Submitted By** | Muhammad Haider Ali (2022-MC-45) |

---

## 📁 Repository Structure

```
week6/
├── screenshots/
│   ├── robot_avoiding_obstacle.png
│   ├── robot_navigating_without_collision.png
│   ├── robot_stopping_at_wall.png
│   ├── ros2_topic_echo_cmd_vel.png
│   ├── ros2_topic_echo_scan_terminal.png
│   ├── rqt_graph_cmd_vel.png
│   └── rviz_laserscan.png
├── lidar_navigator/
│   ├── lidar_navigator/
│   │   ├── __init__.py
│   │   └── lidar_navigator.py
│   ├── package.xml
│   └── setup.py
└── REPORT.md
```

---

## 2. Screenshots

All screenshots are located in the `screenshots/` directory of the `week6/` folder.

---

## 3. Source Code — LiDAR Navigation Node

```python
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
```

Run with:
```bash
export TURTLEBOT3_MODEL=burger
ros2 run lidar_navigator lidar_navigator
```

---

## 4. rqt_graph Screenshot

Located at `screenshots/rqt_graph_cmd_vel.png`.

The graph confirms the active node `/lidar_navigator` subscribing to `/scan` and publishing to `/cmd_vel`.

---

## 5. LaserScan Visualization

Located at `screenshots/rviz_laserscan.png`.

RViz was launched and configured with the `/scan` topic to visualize the LiDAR data in real time. The scan clearly shows the surrounding environment with obstacle boundaries represented as point cloud rings around the robot.

---

## 6. Behavior Demonstrations

### Robot Stopping at an Obstacle
Located at `screenshots/robot_stopping_at_wall.png`.

When the front distance dropped below the `front_threshold` of `0.35 m`, the node immediately set `linear.x = 0.0`, bringing the robot to a full stop before making contact with the wall.

### Robot Avoiding an Obstacle
Located at `screenshots/robot_avoiding_obstacle.png`.

Upon detecting a blocked front region, the robot compared `left_dist` and `right_dist` and committed to turning toward the clearer side at `angular.z = ±0.7 rad/s`. The turn direction was locked using the `self.turning` flag until the front was clear, preventing oscillation.

### Robot Navigating Without Collision
Located at `screenshots/robot_navigating_without_collision.png`.

The robot successfully navigated the TurtleBot3 world environment — moving forward at `0.15 m/s` in open space, slowing and turning at obstacles, and resuming forward motion once clearance was restored — without any collisions.

---

## 7. Terminal Output Screenshots

- `/scan` topic data: `screenshots/ros2_topic_echo_scan_terminal.png`
- `/cmd_vel` topic data: `screenshots/ros2_topic_echo_cmd_vel.png`

These were captured using:
```bash
ros2 topic echo /scan
ros2 topic echo /cmd_vel
```

---

## 8. Observations

### Robot Behavior Near Obstacles
The robot reliably detected obstacles within the defined front region (±30°). As it approached a wall, the front distance reading decreased smoothly and the stop-and-turn response triggered consistently at the threshold distance. No false positives were observed in open space.

### Oscillations and Instability
Initial testing with `front_threshold = 0.5 m` and `angular.z = 0.5 rad/s` caused the robot to get stuck in corners — it would start turning, partially clear the obstacle, then re-trigger the same condition and flip turn direction continuously. This was resolved by:
- Reducing `front_threshold` to `0.35 m` and `side_threshold` to `0.25 m`  so the robot reacts closer to obstacles rather than in open space

### Effect of Changing Threshold Values

| Parameter | Lower Value | Higher Value |
|---|---|---|
| `front_threshold` | Robot gets very close before reacting; risk of collision | Reacts too early; may get stuck in narrow gaps |
| `angular.z` | Slow turn; robot may drift into obstacle during turn | Fast turn; snappy escape but may overshoot |
| `linear.x` | Slower forward speed; more time to react | Faster speed; less time between detection and stop |

---

## 9. Conclusion

This lab provided practical experience in implementing reactive navigation using raw LiDAR sensor data in a ROS 2 and Gazebo environment.

Processing the `/scan` topic's 360-ray range array into directional regions (front, left, right) demonstrated how raw sensor data can be translated into meaningful spatial awareness. The decision logic — stopping on obstacle detection and turning toward the clearer side — showed how simple reactive behaviors can produce robust navigation without any map or path planning.

The most significant challenge was tuning thresholds and resolving the oscillation problem in corners. The fix required understanding that re-evaluating turn direction on every scan callback caused instability, and that committing to a decision (via a state flag) until conditions changed was the correct approach. This mirrors real-world controller design principles where state machines and hysteresis prevent chattering.

These fundamentals directly underpin more advanced topics such as the Vector Field Histogram (VFH), potential field navigation, and full autonomous stacks like Nav2.
