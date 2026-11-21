import math
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory

try:
    import serial
except ImportError:
    serial = None


class ServoHardwareBridge(Node):
    def __init__(self):
        super().__init__("servo_bridge_node")
        self.declare_parameter("port", "/dev/ttyUSB0")
        self.declare_parameter("baudrate", 115200)
        self.declare_parameter("min_deg", 0.0)
        self.declare_parameter("max_deg", 180.0)
        self.declare_parameter("dry_run", True)

        port = self.get_parameter("port").value
        baudrate = int(self.get_parameter("baudrate").value)
        self.min_deg = float(self.get_parameter("min_deg").value)
        self.max_deg = float(self.get_parameter("max_deg").value)
        self.dry_run = bool(self.get_parameter("dry_run").value)

        self.ser = None
        if not self.dry_run and serial is not None:
            try:
                self.ser = serial.Serial(port, baudrate, timeout=0.1)
                self.get_logger().info(f"Connected to microcontroller on {port} @ {baudrate}")
            except Exception as exc:
                self.get_logger().warn(f"Serial open failed ({exc}); continuing in log/dry mode")

        self.sub = self.create_subscription(
            JointTrajectory,
            "/arm_controller/joint_trajectory",
            self.trajectory_callback,
            10,
        )
        self.get_logger().info("Listening on /arm_controller/joint_trajectory")

    def rad_to_clamped_deg(self, rad_val: float) -> float:
        deg_val = math.degrees(rad_val) + 90.0
        return max(self.min_deg, min(self.max_deg, deg_val))

    def trajectory_callback(self, msg: JointTrajectory):
        if not msg.points:
            return
        point = msg.points[0]
        names = msg.joint_names if msg.joint_names else [f"joint{i+1}" for i in range(len(point.positions))]

        angles_deg = []
        for idx, rad_pos in enumerate(point.positions):
            clamped = round(self.rad_to_clamped_deg(rad_pos), 2)
            joint_name = names[idx] if idx < len(names) else f"joint{idx+1}"
            angles_deg.append((joint_name, clamped))

        line = "JOINTS:" + ",".join(f"{name}={ang}" for name, ang in angles_deg) + "\n"
        self.get_logger().info(f"Servo command -> {line.strip()}")

        if self.ser is not None and self.ser.is_open:
            try:
                self.ser.write(line.encode("utf-8"))
            except Exception as exc:
                self.get_logger().warn(f"Serial write error: {exc}")

    def destroy_node(self):
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ServoHardwareBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
