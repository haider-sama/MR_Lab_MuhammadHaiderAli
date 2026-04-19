# MCT-454L Mobile Robotics — Lab Manual #04
### Introduction to ROS 2 Launch, Rosbag, rqt-plot

| | |
|---|---|
| **Submitted To** | Dr. Maria Akram |
| **Submitted By** | Muhammad Haider Ali (2022-MC-45) |

---

## 📁 Repository Structure

```
week4/
├── screenshots/
│   └── rqt_plot_graph.png
├── ros2_ws/
│   └── src/
│       └── my_launch_pkg/
│           └── launch/
│               └── turtlesim_launch.py
└── REPORT.md
```

---

## Approach & Observations

This lab focused on ROS 2 launch files, rosbag recording, rqt visualization, and implementing a follow-the-leader behavior in turtlesim.

- A launch file was created to start the turtlesim simulation and teleoperation node simultaneously
- A second turtle was spawned via the `/spawn` service for multi-robot interaction
- Rosbag2 recorded `/turtle1/pose`, `/turtle2/pose`, `/turtle1/cmd_vel`, `/turtle2/cmd_vel` — replayed successfully to reproduce movements
- A follow-the-leader node was implemented where `turtle2` subscribes to `turtle1`'s pose and publishes velocity commands to follow it
- `rqt_plot` was used to visualize `/turtle1/cmd_vel` in real time

**Key Findings:**
- Launch system simplifies multi-node execution
- Rosbag is useful for recording and replaying robot behavior
- Pose-based control enables basic multi-robot coordination
- `rqt_plot` helps analyze motion commands visually

---

## Rosbag Recording

```bash
ros2 bag record /turtle1/pose /turtle2/pose /turtle1/cmd_vel /turtle2/cmd_vel
```

**Trajectory Observations:**
- `turtle1` shows continuous trajectory based on keyboard input
- `turtle2` follows `turtle1` with a slight delay
- Path similarity confirms successful follower behavior
- Small tracking error exists due to proportional control

---

## Follow-the-Leader Code

```python
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

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
```

---

## rqt_plot Graph

The graph screenshot is located in screenshots/rqt_plot_graph.png
