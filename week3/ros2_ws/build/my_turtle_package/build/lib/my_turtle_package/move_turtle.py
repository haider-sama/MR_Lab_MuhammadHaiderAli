import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
import math
import time

class VelocityPublisher(Node):

    def __init__(self):
        super().__init__('velocity_publisher')

        # Turtle1 (triangle motion)
        self.publisher1_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer1 = self.create_timer(0.1, self.timer_callback_turtle1)
        self.state = 0
        self.counter = 0

        # Turtle2 (circular motion)
        self.publisher2_ = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.timer2 = self.create_timer(0.1, self.timer_callback_turtle2)
        self.start_time2 = time.time()

        # Turtle3 (sinusoidal motion)
        self.publisher3_ = self.create_publisher(Twist, '/turtle3/cmd_vel', 10)
        self.timer3 = self.create_timer(0.1, self.timer_callback_turtle3)
        self.start_time3 = time.time()

        # Spawn turtles 2 and 3
        self.spawn_turtle('turtle2', 5.0, 5.0)
        self.spawn_turtle('turtle3', 8.0, 8.0)

    # Turtle1: triangle motion
    def timer_callback_turtle1(self):
        msg = Twist()

        if self.state == 0:
            msg.linear.x = 2.0
            msg.angular.z = 0.0
            self.counter += 1
            if self.counter > 20:
                self.state = 1
                self.counter = 0

        elif self.state == 1:
            msg.linear.x = 0.0
            msg.angular.z = 1.57
            self.counter += 1
            if self.counter > 10:
                self.state = 0
                self.counter = 0

        self.publisher1_.publish(msg)

    # Turtle2: circular motion
    def timer_callback_turtle2(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.publisher2_.publish(msg)

    # Turtle3: sinusoidal motion (forward speed constant, angular oscillates)
    def timer_callback_turtle3(self):
        t = time.time() - self.start_time3
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = math.sin(t * 2.0)  # angular oscillates sinusoidally
        self.publisher3_.publish(msg)

    # Generic turtle spawn
    def spawn_turtle(self, name, x, y):
        client = self.create_client(Spawn, '/spawn')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f'Waiting for /spawn service for {name}...')

        req = Spawn.Request()
        req.x = x
        req.y = y
        req.theta = 0.0
        req.name = name

        future = client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info(f"Spawned {future.result().name}")
        else:
            self.get_logger().error(f"Failed to spawn {name}")


def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()