# MCT-454L Mobile Robotics — Lab Manual #02
### ROS, Packages, Nodes, Topics, Services, RQT

| | |
|---|---|
| **Submitted To** | Dr. Maria Akram |
| **Submitted By** | Muhammad Haider Ali (2022-MC-45) |

---

## 📁 Repository Structure

```
week2/
├── screenshots/
│   ├── turtlesim_launch.png
│   ├── turtle_teleop.png
│   ├── topic_echo_pose.png
│   ├── cmd_vel_publish.png
│   ├── service_reset.png
│   ├── rqt_graph.png
│   ├── rqt_spawn.png
│   ├── turtle2_control.png
│   └── service_experiment.png
└── REPORT.md
```

---

## Lab Setup

```bash
source /opt/ros/humble/setup.bash
sudo apt install ros-humble-turtlesim
```

---

## Step-by-Step Observations

**Step 1 — Launch Turtlesim**
```bash
ros2 run turtlesim turtlesim_node
```
Single turtle appears in the center of a blue background.

**Step 2 — Keyboard Teleoperation**
```bash
ros2 run turtlesim turtle_teleop_key
```
Turtle responds to arrow key input as expected.

**Step 3 — Explore Topics**
```bash
ros2 topic list
ros2 topic echo /turtle1/pose
```
Real-time position updates `(x, y, theta)` printed continuously to terminal.

**Step 4 — Publish Velocity Commands**
```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"
```
Turtle moves in a curved arc based on the linear and angular velocity values.

**Step 5 — Reset Simulation**
```bash
ros2 service call /reset std_srvs/srv/Empty
```
Turtle returns to its starting position.

---

## rqt & Services

**Open rqt**
```bash
rqt
```
All active nodes, topics, and services visible via `Plugins → Topics / Services / Nodes`.

**Spawn a second turtle via rqt**

Navigate to the Services tab → call `/spawn` with:
```
x: 5.0, y: 5.0, theta: 0.0, name: 'turtle2'
```
`turtle2` spawns at the specified coordinates.

**Control Turtle2**
```bash
ros2 topic pub /turtle2/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 1.0}, angular: {z: 1.0}}"
```
`turtle2` moves independently of `turtle1`.

**Other Services Explored**
- `/set_background_color` — changes the simulation background color
- `/turtle1/teleport_absolute` — instantly moves turtle to a target pose
- `/turtle1/teleport_relative` — moves turtle relative to its current pose

---

## Key Observations

- ROS 2 topics allow real-time monitoring of robot state
- Services handle discrete actions like spawning, resetting, and teleporting
- `rqt` simplifies inspection of nodes, topics, and services without terminal commands
- Multiple turtles can be controlled independently on separate topics

---

## Problems Faced

- `turtlesim_node` failed to launch initially — fixed by sourcing the ROS 2 environment
- Spawning `turtle2` required correct values for `x`, `y`, `theta`, and a unique `name`

---

## Conclusion

ROS 2 CLI tools and the `rqt` GUI together provide full control over simulated robots. This lab solidified understanding of the node-topic-service architecture that underpins all ROS 2 applications.
