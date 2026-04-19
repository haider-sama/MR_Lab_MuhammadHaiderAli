# MCT-454L Mobile Robotics — Lab Manual #03
### ROS 2 Workspace Setup, Package Creation, and GitHub Introduction

| | |
|---|---|
| **Submitted To** | Dr. Maria Akram |
| **Submitted By** | Muhammad Haider Ali (2022-MC-45) |

---

## 📁 Repository Structure

```
week3/
├── ros2_ws/
│   └── src/
│       └── my_turtle_package/
│           └── my_turtle_package/
│               ├── triangle_node.py
│               ├── circle_node.py
│               └── sinusoidal_node.py
├── screenshots/
└── REPORT.md
```

---

## Lab Setup

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

Created a ROS 2 Python package named `my_turtle_package` with dependencies `rclpy` and `turtlesim`. Configured Git, initialized the repository, linked to GitHub, and pushed the first commit.

---

## Step-by-Step Observations

**Step 1 — Launch Turtlesim**
```bash
ros2 run turtlesim turtlesim_node
```
Single turtle appears in the center of a blue background.

**Step 2 — Explore ROS 2 Topics**
```bash
ros2 topic list
ros2 topic echo /turtle1/pose
```
`turtle1`'s position and orientation are published continuously on `/turtle1/pose`.

**Step 3 — Triangle Motion (Turtle1)**
A `VelocityPublisher` node drives `turtle1` in a triangular pattern using alternating linear and angular velocities. Turtle follows the intended path correctly.

**Step 4 — Spawn Turtle2 (Circular Motion)**
```bash
ros2 service call /spawn turtlesim/srv/Spawn "{x: 5.0, y: 5.0, theta: 0.0, name: 'turtle2'}"
```
`turtle2` spawns at `(5, 5)` and moves in a circular pattern via a dedicated Python node.

**Step 5 — Spawn Turtle3 (Sinusoidal Motion)**
```bash
ros2 service call /spawn turtlesim/srv/Spawn "{x: 8.0, y: 8.0, theta: 0.0, name: 'turtle3'}"
```
`turtle3` follows a wavy sinusoidal trajectory using `math.sin()` for angular velocity.

**Step 6 — Teleport Turtle1**
```bash
ros2 service call /turtle1/teleport_absolute turtlesim/srv/TeleportAbsolute "{x: 5.5, y: 5.5, theta: 0.0}"
```
`turtle1` instantly moves to the target location for clean screenshots.

---

## Key Observations

- ROS 2 topics allow real-time monitoring of turtle positions and velocities
- Services like `/spawn` and `/teleport_absolute` enable direct turtle manipulation
- Multiple turtles move independently without interfering with each other
- Python nodes effectively automate complex motion patterns

---

## Problems Faced

- `turtlesim_node` failed to launch initially — fixed by correctly sourcing the ROS 2 environment
- Spawning required exact coordinates, orientation, and unique names
- Managing separate publishers and timers per turtle was needed for independent control
- `git push` failed due to branch being behind remote — resolved with `git pull --rebase`

---

## Conclusion

This lab reinforced practical knowledge of ROS 2 workspaces, nodes, topics, and services. Version control with Git and GitHub integrated well into the ROS 2 workflow. All three motion patterns (triangular, circular, sinusoidal) were successfully implemented and all objectives of Lab Manual #03 were fully achieved.

---

## Screenshots

All screenshots are located in the `screenshots/` directory with respective step and task names.
