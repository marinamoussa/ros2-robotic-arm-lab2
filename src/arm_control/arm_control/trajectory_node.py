import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class ArmTrajectoryPublisher(Node):
    def __init__(self):
        super().__init__("arm_trajectory_publisher")
        self.pub = self.create_publisher(
            JointTrajectory, "/arm_controller/joint_trajectory", 10
        )
        self.timer = self.create_timer(3.0, self.send_trajectory)
        self.step = 0

    def send_trajectory(self):
        poses = [
            [0.4, -0.3, 0.3, 0.2],
            [-0.4, 0.3, -0.3, -0.2],
            [0.0, 0.0, 0.0, 0.0],
        ]
        msg = JointTrajectory()
        msg.joint_names = ["joint1", "joint2", "joint3", "joint4"]

        point = JointTrajectoryPoint()
        point.positions = poses[self.step % len(poses)]
        point.velocities = []
        point.accelerations = []
        point.effort = []
        point.time_from_start = Duration(sec=1, nanosec=500000000)

        msg.points = [point]
        self.pub.publish(msg)
        self.get_logger().info(f"Published trajectory: {point.positions}")
        self.step += 1


def main(args=None):
    rclpy.init(args=args)
    node = ArmTrajectoryPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
