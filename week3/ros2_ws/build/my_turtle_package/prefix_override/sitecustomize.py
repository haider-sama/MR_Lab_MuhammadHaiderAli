import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/media/haider/Storage/University Work/semester_08/mobile_robotics/MR_Lab_MuhammadHaiderAli/week3/ros2_ws/install/my_turtle_package'
