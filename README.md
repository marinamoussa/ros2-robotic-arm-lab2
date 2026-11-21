# 4-DOF Robotic Arm (ROS 2 Jazzy, RViz2, Gazebo Sim & Hardware Bridge)

## Overview
4-DOF robotic arm (8 cm base, 12 cm L1, 15 cm L2, 9 cm L3, 6 cm end effector) with RViz2, Gazebo (gz sim), `/arm_controller/joint_trajectory`, and serial PWM servo control.

## Workspace Structure
- `src/arm_description`: URDF and RViz2 launch files.
- `src/arm_gazebo`: Gazebo world (`arm_world.sdf`) and launch files.
- `src/arm_control`: `trajectory_node`, `slider_trajectory_gui`, and `trajectory_to_gz_bridge`.
- `src/arm_hardware_bridge`: `servo_bridge_node` (radians to clamped `0-180` deg serial `JOINTS:...`).
- `firmware/servo_controller.ino`: Microcontroller PWM servo sketch (`115200` baud).

## Dependencies
- Ubuntu 24.04 LTS, ROS 2 Jazzy (`rclpy`, `trajectory_msgs`, `sensor_msgs`, `std_msgs`, `builtin_interfaces`, `robot_state_publisher`, `joint_state_publisher_gui`, `rviz2`, `ros_gz_sim`, `ros_gz_bridge`).
- Python `pyserial` and `tkinter` (`python3-tk`), plus microcontroller `Servo` library.

## Build & Run
~~~~bash
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws
colcon build
source ~/ros2_ws/install/setup.bash
~~~~

~~~~bash
ros2 launch arm_description view_arm.launch.py
gz sim -r ~/ros2_ws/install/arm_gazebo/share/arm_gazebo/worlds/arm_world.sdf
ros2 run arm_control trajectory_to_gz_bridge
ros2 run arm_control slider_trajectory_gui
ros2 run arm_hardware_bridge servo_bridge_node
~~~~

## Transport & Message Format
- Topic: `/arm_controller/joint_trajectory` (`trajectory_msgs/msg/JointTrajectory`) with `joint_names` (`joint1`..`joint4`), `points[0].positions` in radians, `time_from_start`, and empty `velocities`/`accelerations`/`effort`.
- Serial (`115200` baud): `JOINTS:joint1=<deg>,joint2=<deg>,joint3=<deg>,joint4=<deg>\n` clamped to `[0.0, 180.0]` degrees.

## Pin Mapping (Common Ground Required)
| Board Pin | Connects To | Notes |
| :--- | :--- | :--- |
| Pin `3` | Servo 1 (`joint1`) signal | PWM |
| Pin `5` | Servo 2 (`joint2`) signal | PWM |
| Pin `6` | Servo 3 (`joint3`) signal | PWM |
| Pin `9` | Servo 4 (`joint4`) signal | PWM |
| Shared `GND` | MCU GND, servo PSU GND, servo GND | Common ground |
