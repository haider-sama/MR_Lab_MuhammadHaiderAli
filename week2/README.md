# Week 2 - Mobile Robotics Lab

## Lab Activities
Lab 2 focused on ROS 2 topics, services, nodes, and using the rqt GUI with the Turtlesim simulator.

## Steps Followed
1. Launch Turtlesim node (`ros2 run turtlesim turtlesim_node`).  
2. Control the turtle using keyboard teleoperation (`ros2 run turtlesim turtle_teleop_key`).  
3. Explore ROS 2 topics using `ros2 topic list` and `ros2 topic echo /turtle1/pose`.  
4. Send velocity commands using `ros2 topic pub /turtle1/cmd_vel`.  
5. Reset the simulation using `/reset` service.  
6. Open rqt and explore nodes, topics, and services.  
7. Spawn a second turtle and control it independently.  
8. Experiment with other services (`/clear`, `/set_background_color`, `/teleport_absolute`).  

## Commands Used
- `ros2 run turtlesim turtlesim_node`  
- `ros2 run turtlesim turtle_teleop_key`  
- `ros2 topic list`  
- `ros2 topic echo /turtle1/pose`  
- `ros2 topic pub /turtle1/cmd_vel`  
- `ros2 service call /reset std_srvs/srv/Empty`  
- `rqt`  

## Problems Faced
- Initial launch failed until ROS 2 environment was sourced.  
- Correct parameter input required for spawning second turtle.  

## Reflection
This lab helped me understand how ROS 2 nodes, topics, and services interact in a simulated environment.  
Using rqt made visualization and service calls straightforward.  
The experience improved confidence in controlling robots in simulation and using ROS 2 CLI commands effectively.