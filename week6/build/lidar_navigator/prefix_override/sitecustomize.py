import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/media/haider/Drive1/University Work/semester_08/mobile_robotics/MR_Lab_MuhammadHaiderAli/week6/install/lidar_navigator'
