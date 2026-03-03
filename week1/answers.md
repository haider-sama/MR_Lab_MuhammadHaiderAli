# Week 1 Post Lab Answers

1. Node: A process in ROS 2 that performs computation.
   Topic: A named communication channel that enables message passing between users.
   Package: A folder that contains ROS 2 code together with its metadata and necessary dependencies.
   Workspace: A directory that contains multiple ROS 2 packages together with their build results.

2. Sourcing sets environment variables which enable ROS 2 to find installed packages.
   Without sourcing, ROS 2 cannot find packages or executables.

3. colcon build compiles and installs packages inside the workspace.
   The system creates three directories which include build/, install/, and log/ folders.

4. The console_scripts entry point registers a Python function as a runnable executable which enables ros2 run to find and execute the function.

5. Publisher/Subscriber Diagram:

   Node A (Publisher) ---> /topic_name ---> Node B (Subscriber)
