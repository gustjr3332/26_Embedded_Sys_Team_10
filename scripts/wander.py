"""SLAM용 장애물 회피 배회 주행. 바닥에서만 쓴다(라이다는 책상 끝 낭떠러지를 못 본다).
실물: python3 scripts/wander.py [초=240]
시뮬: python3 scripts/wander.py 240 --ros-args -p use_sim_time:=true
"""
import sys, time, math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.utilities import remove_ros_args
from rclpy.signals import SignalHandlerOptions
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan

# 실물 기준 보수적인 값. 넓고 안전한 공간이면 올려도 된다.
FWD, SLOW, TURN = 0.12, 0.08, 0.6      # m/s, m/s, rad/s
FRONT_STOP, SIDE_KEEP = 0.40, 0.25     # m
SCAN_TIMEOUT = 0.5                     # s, 스캔이 끊기면 정지


class Wander(Node):
    def __init__(self):
        super().__init__('wander')
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.create_subscription(LaserScan, '/scan', self.on_scan, qos_profile_sensor_data)
        self.turn_dir = 1.0
        self.last_scan = time.time()
        self.create_timer(0.1, self.watchdog)

    def sector(self, msg, lo, hi):
        # 각도(도)로 인덱스를 구한다. LDS-02는 한 바퀴 점 개수가 매번 조금씩 달라서 고정 인덱스를 쓰면 안 된다.
        n = len(msg.ranges)
        vals = []
        for deg in range(lo, hi + 1):
            i = int(round((math.radians(deg) - msg.angle_min) / msg.angle_increment)) % n
            r = msg.ranges[i]
            if math.isfinite(r) and r > max(msg.range_min, 0.05):
                vals.append(r)
        return min(vals) if vals else 3.5

    def send(self, vx=0.0, wz=0.0):
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
        cmd.twist.linear.x, cmd.twist.angular.z = vx, wz
        self.pub.publish(cmd)

    def watchdog(self):
        if time.time() - self.last_scan > SCAN_TIMEOUT:
            self.send()

    def on_scan(self, msg):
        if not msg.ranges or msg.angle_increment <= 0:
            return
        self.last_scan = time.time()
        front = min(self.sector(msg, -25, 25), 3.5)
        left = self.sector(msg, 30, 90)
        right = self.sector(msg, -90, -30)
        if front < FRONT_STOP:
            self.turn_dir = 1.0 if left > right else -1.0
            self.send(0.0, TURN * self.turn_dir)
        elif left < SIDE_KEEP:
            self.send(SLOW, -TURN / 2)
        elif right < SIDE_KEEP:
            self.send(SLOW, TURN / 2)
        else:
            self.send(FWD, 0.15 * self.turn_dir)


# rclpy 기본 SIGINT 핸들러는 Ctrl+C 때 컨텍스트를 먼저 꺼서 정지 명령 발행이 실패한다.
# 터틀봇은 마지막 /cmd_vel을 계속 유지하므로 직접 KeyboardInterrupt로 받아 정지를 보낸다.
rclpy.init(args=sys.argv, signal_handler_options=SignalHandlerOptions.NO)
args = remove_ros_args(sys.argv)
duration = float(args[1]) if len(args) > 1 else 240.0
node = Wander()
end = time.time() + duration
try:
    while rclpy.ok() and time.time() < end:
        rclpy.spin_once(node, timeout_sec=0.1)
except KeyboardInterrupt:
    pass
finally:
    for _ in range(3):  # Ctrl+C나 시간 종료 시 확실히 멈춘다
        node.send()
        time.sleep(0.05)
    node.destroy_node()
    rclpy.try_shutdown()
