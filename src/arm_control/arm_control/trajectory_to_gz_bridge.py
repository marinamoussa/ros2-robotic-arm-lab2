import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from trajectory_msgs.msg import JointTrajectory


class TrajectoryToGzBridge(Node):
    def __init__(self):
        super().__init__("trajectory_to_gz_bridge")
        self.joint_names = ["joint1", "joint2", "joint3", "joint4"]
        self.pubs = {
            name: self.create_publisher(
                Float64, f"/gz_cmd/{name}", 10
            )
            for name in self.joint_names
        }
        self.sub = self.create_subscription(
            JointTrajectory,
            "/arm_controller/joint_trajectory",
            self.cb,
            10,
        )
        self.get_logger().info("Relaying /arm_controller/joint_trajectory -> /gz_cmd/joint1..4")

    def cb(self, msg: JointTrajectory):
        if not msg.points:
            return
        pt = msg.points[0]
        names = msg.joint_names if msg.joint_names else self.joint_names
        for idx, pos in enumerate(pt.positions):
            if idx < len(names) and names[idx] in self.pubs:
                out = Float64()
                out.data = float(pos)
                self.pubs[names[idx]].publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryToGzBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
