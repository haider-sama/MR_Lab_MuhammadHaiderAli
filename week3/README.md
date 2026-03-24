# Week 3 - Mobile Robotics Lab

## Lab Activities
Lab 3 focused on extending control of turtlesim by automating turtle motion using Python nodes.  
The lab included moving turtles in triangular, circular, and sinusoidal patterns, spawning multiple turtles, and teleporting a turtle to a specific location.  

## Steps Followed
1. Launch Turtlesim node (`ros2 run turtlesim turtlesim_node`).  
2. Explore ROS 2 topics using `ros2 topic list` and `ros2 topic echo /turtle1/pose`.  
3. Send velocity commands using Python node to move Turtle1 in a triangular pattern.  
4. Spawn Turtle2 at specific coordinates (`ros2 service call /spawn`) and move it in a circular path.  
5. Spawn Turtle3 at specific coordinates and control it to move in a sinusoidal path using `math.sin()` for angular velocity.  
6. Observe all three turtles moving simultaneously and independently.  
7. Teleport Turtle1 to a precise location (`ros2 service call /turtle1/teleport_absolute`) for taking clean screenshots.  

## Commands Used
- `ros2 run turtlesim turtlesim_node`  
- `ros2 topic list`  
- `ros2 topic echo /turtle1/pose`  
- `ros2 service call /spawn turtlesim/srv/Spawn "{x: 5.0, y: 5.0, theta: 0.0, name: 'turtle2'}"`  
- `ros2 service call /spawn turtlesim/srv/Spawn "{x: 8.0, y: 8.0, theta: 0.0, name: 'turtle3'}"`  
- `ros2 service call /turtle1/teleport_absolute turtlesim/srv/TeleportAbsolute "{x: 5.5, y: 5.5, theta: 0.0}"`  
- `ros2 run my_turtle_package move_turtle.py`  

## Problems Faced
- `turtlesim_node` initially failed to launch until ROS 2 environment was sourced.  
- Correct coordinates, theta, and unique names were required when spawning additional turtles.  
- Synchronizing multiple turtles’ motion in a single node required careful handling of separate publishers and timers.  
- Git push failed initially due to local branch being behind remote; fixed using `git pull --rebase` before pushing.  

## Reflection
This lab reinforced understanding of ROS 2 nodes, topics, and services in a simulated environment.  
Automating turtle motion with Python nodes improved efficiency in testing complex patterns.  
Multiple turtles could be controlled independently, and teleporting turtles allowed precise positioning for screenshots.  
Confidence in using ROS 2 CLI commands and services, as well as GitHub integration for version control, was strengthened.
