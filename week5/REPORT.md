# MCT-454L Mobile Robotics — Lab Manual #05
### Introduction to Gazebo and RViz with ROS 2 using TurtleBot3

| | |
|---|---|
| **Submitted To** | Dr. Maria Akram |
| **Submitted By** | Muhammad Haider Ali (2022-MC-45) |

---

## 📁 Repository Structure

```
week5/
├── screenshots/
│   ├── deliverable_4.png       # rqt_graph output
│   ├── deliverable_6.png       # cmd_vel publisher output
│   └── deliverable_7.png       # odom subscriber output
├── rosbag2_2026_04_19-19_52_01/  # Recorded ros2 bag file
├── maps/
│   ├── my_map.pgm              # SLAM-generated map image
│   └── my_map.yaml             # Map metadata
├── cmd_vel_publisher.py
├── odom_subscriber.py
└── REPORT.md
```

---

## 2. Screenshots

All screenshots are located in the `screenshots/` directory of the `week5/` folder.

---

## 3. Recorded ros2 bag file

The bag recording is located in `rosbag2_2026_04_19-19_52_01/` directory.

To replay:
```bash
ros2 bag play rosbag2_2026_04_19-19_52_01/
```

---

## 4. rqt_graph Screenshot

Located at `screenshots/deliverable_4.png`.

---

## 5. Observations on Discrepancies

Several discrepancies were observed between expected and simulated robot behavior:

- **Odometry Drift** — Over extended navigation paths, wheel odometry accumulated significant error. The robot's RViz position diverged from the actual Gazebo position, demonstrating why pure odometry is insufficient for localization.
- **Velocity Overshoot** — When forward velocity commands were issued via teleop, the robot briefly overshot before stabilizing due to Gazebo's inertia simulation.
- **Return to Origin Imprecision** — Navigating the robot back to `(0, 0, 0)` using teleoperation and odometry feedback was challenging due to accumulated drift. The odometry reading differed from the Gazebo ground truth by approximately `0.05–0.1 m` after a full exploration session.
- **LiDAR Noise** — The simulated LiDAR scan showed minor noise consistent with real sensor behavior. This had negligible impact on mapping quality.
- **Map Latency** — The occupancy grid map in RViz updated with a slight delay behind actual robot movement, as Cartographer processes scan data in batches.

---

## 6. cmd_vel Publisher

> Screenshot of running output: `screenshots/deliverable_6.png`

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelPublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.moving = False
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
```

Run with:
```bash
python3 cmd_vel_publisher.py
```

---

## 7. Odom Subscriber

> Screenshot of running output: `screenshots/deliverable_7.png`

```python
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
```

Run with:
```bash
python3 odom_subscriber.py
```

---

## 8. Conclusion

This lab provided essential hands-on experience with the core simulation and visualization stack used in modern ROS 2 robotics development.

**Gazebo** proved to be a highly capable simulation environment, accurately modeling the TurtleBot3's differential drive kinematics, LiDAR sensor behavior, and environmental interactions.

**RViz** served as an indispensable debugging and analysis tool. Simultaneously visualizing multiple data streams (LaserScan, TF frames, Odometry, and the Cartographer map) gave a comprehensive picture of robot state that would be impossible to obtain from terminal output alone.

**Google Cartographer** demonstrated the power of SLAM — the robot autonomously built an accurate occupancy grid map of the environment while continuously correcting its own position estimate. The contrast between raw odometry (which drifted noticeably) and the SLAM-corrected pose highlighted why sensor fusion and loop closure are essential for reliable robot navigation.

Implementing the `cmd_vel` publisher and `odom` subscriber reinforced fundamental ROS 2 programming patterns: creating nodes, defining timer callbacks, and using typed message interfaces to interact with the robot.

### Challenges Faced

- Synchronizing simulation time with `use_sim_time:=true` required careful setup — forgetting this flag caused Cartographer to reject incoming sensor data.
- Navigating the robot back to `(0, 0, 0)` purely from odometry feedback was difficult due to drift accumulation.
- Gazebo's startup time was significant on the lab machine; patience was required before the simulation was ready.
- RViz plugin configuration (fixed frame, topic names, QoS settings) needed careful attention to ensure data displayed correctly.
