import threading
import tkinter as tk
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class SliderTrajectoryGui(Node):
    def __init__(self):
        super().__init__("slider_trajectory_gui")
        self.pub = self.create_publisher(
            JointTrajectory, "/arm_controller/joint_trajectory", 10
        )
        self.joint_names = ["joint1", "joint2", "joint3", "joint4"]

    def publish_positions(self, positions_rad):
        msg = JointTrajectory()
        msg.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = [float(x) for x in positions_rad]
        point.velocities = []
        point.accelerations = []
        point.effort = []
        point.time_from_start = Duration(sec=1, nanosec=0)

        msg.points = [point]
        self.pub.publish(msg)
        self.get_logger().info(f"GUI published: {point.positions}")


def main(args=None):
    rclpy.init(args=args)
    node = SliderTrajectoryGui()

    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()

    root = tk.Tk()
    root.title("4-DOF Arm Trajectory Sliders")

    sliders = []

    def on_change(_val=None):
        vals = [s.get() for s in sliders]
        node.publish_positions(vals)

    for idx, jname in enumerate(node.joint_names):
        tk.Label(root, text=f"{jname} (rad)").grid(row=idx, column=0, padx=10, pady=6, sticky="w")
        scale = tk.Scale(
            root,
            from_=-1.57,
            to=1.57,
            resolution=0.02,
            orient=tk.HORIZONTAL,
            length=260,
            command=on_change,
        )
        scale.set(0.0)
        scale.grid(row=idx, column=1, padx=10, pady=6)
        sliders.append(scale)

    def reset_zero():
        for s in sliders:
            s.set(0.0)
        on_change()

    tk.Button(root, text="Center / Zero", command=reset_zero).grid(
        row=len(node.joint_names), column=0, columnspan=2, pady=10
    )

    try:
        root.mainloop()
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
