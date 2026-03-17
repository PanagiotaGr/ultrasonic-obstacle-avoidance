import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from collections import deque
import statistics


class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')

        self.left_buffer = deque(maxlen=5)
        self.front_buffer = deque(maxlen=5)
        self.right_buffer = deque(maxlen=5)

        self.left_distance = 10.0
        self.front_distance = 10.0
        self.right_distance = 10.0

        self.safe_distance = 0.40
        self.stop_distance = 0.20

        self.max_linear_speed = 0.20
        self.max_angular_speed = 0.80
        self.side_gain = 0.5

        self.create_subscription(Float32, '/ultra_left', self.left_callback, 10)
        self.create_subscription(Float32, '/ultra_front', self.front_callback, 10)
        self.create_subscription(Float32, '/ultra_right', self.right_callback, 10)

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Obstacle avoidance node started.')

    def median_filter(self, buffer, value):
        if value > 0.0:
            buffer.append(value)

        if len(buffer) == 0:
            return 10.0

        return statistics.median(buffer)

    def left_callback(self, msg):
        self.left_distance = self.median_filter(self.left_buffer, msg.data)

    def front_callback(self, msg):
        self.front_distance = self.median_filter(self.front_buffer, msg.data)

    def right_callback(self, msg):
        self.right_distance = self.median_filter(self.right_buffer, msg.data)

    def control_loop(self):
        cmd = Twist()

        left = self.left_distance
        front = self.front_distance
        right = self.right_distance

        if front <= self.stop_distance:
            cmd.linear.x = 0.0
            if left > right:
                cmd.angular.z = self.max_angular_speed
            else:
                cmd.angular.z = -self.max_angular_speed

        elif front <= self.safe_distance:
            cmd.linear.x = 0.05
            if left > right:
                cmd.angular.z = 0.6
            else:
                cmd.angular.z = -0.6

        else:
            cmd.linear.x = self.max_linear_speed
            side_error = left - right
            cmd.angular.z = self.side_gain * side_error

            if cmd.angular.z > self.max_angular_speed:
                cmd.angular.z = self.max_angular_speed
            elif cmd.angular.z < -self.max_angular_speed:
                cmd.angular.z = -self.max_angular_speed

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
