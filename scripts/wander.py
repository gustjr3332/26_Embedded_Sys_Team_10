import sys, time, math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan

DURATION = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0


class Wander(Node):
    def __init__(self):
        super().__init__('wander', parameter_overrides=[rclpy.parameter.Parameter('use_sim_time', value=True)])
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.create_subscription(LaserScan, '/scan', self.on_scan, qos_profile_sensor_data)
        self.turn_dir = 1.0

    def sector(self, msg, lo, hi):
        n = len(msg.ranges)
        vals = []
        for deg in range(lo, hi + 1):
            r = msg.ranges[int(deg % 360 * n / 360) % n]
            if math.isfinite(r) and r > msg.range_min:
                vals.append(r)
        return min(vals) if vals else 3.5

    def on_scan(self, msg):
        front = min(self.sector(msg, -25, 25), 3.5)
        left = self.sector(msg, 30, 90)
        right = self.sector(msg, -90, -30)
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
        if front < 0.45:
            self.turn_dir = 1.0 if left > right else -1.0
            cmd.twist.angular.z = 0.8 * self.turn_dir
        elif left < 0.3:
            cmd.twist.linear.x = 0.12
            cmd.twist.angular.z = -0.4
        elif right < 0.3:
            cmd.twist.linear.x = 0.12
            cmd.twist.angular.z = 0.4
        else:
            cmd.twist.linear.x = 0.18
            cmd.twist.angular.z = 0.15 * self.turn_dir
        self.pub.publish(cmd)


rclpy.init()
node = Wander()
end = time.time() + DURATION
while rclpy.ok() and time.time() < end:
    rclpy.spin_once(node, timeout_sec=0.1)
node.pub.publish(TwistStamped())
node.destroy_node()
rclpy.shutdown()
