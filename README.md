# 4-DOF Robotic Arm (ROS 2 Jazzy, RViz2, Gazebo Sim & Hardware Bridge)

## Overview
This workspace models a 4-DOF robotic arm (8 cm base height, 12 cm L1, 15 cm L2, 9 cm L3, 6 cm end effector) and connects trajectory commands from ROS 2 to RViz2, Gazebo (gz sim), and real PWM servo hardware over serial.

## Workspace Structure (src/ & firmware/)
- src/arm_description: URDF model (urdf/arm.urdf) and visualization launch files (launch/view_arm.launch.py).
- src/arm_gazebo: Gazebo world SDF (worlds/arm_world.sdf) with joint position controllers and launch files.
- src/arm_control: Python nodes (trajectory_node, slider_trajectory_gui, trajectory_to_gz_bridge) publishing/relaying trajectory_msgs/msg/JointTrajectory.
- src/arm_hardware_bridge: Python serial bridge (servo_bridge_node) converting radians to clamped servo degrees (0-180 deg).
- firmware/servo_controller.ino: Microcontroller serial PWM firmware parsing JOINTS:... commands.

## Dependencies
- Ubuntu 24.04 LTS with ROS 2 Jazzy (rclpy, trajectory_msgs, sensor_msgs, std_msgs, builtin_interfaces, robot_state_publisher, joint_state_publisher_gui, rviz2, ros_gz_sim, ros_gz_bridge)
- Python pyserial (pip install pyserial) and tkinter (python3-tk)
- Microcontroller IDE / toolchain with Servo library

## Build Instructions
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws
colcon build
source ~/ros2_ws/install/setup.bash

## Topic & Message Format
- Trajectory Topic: /arm_controller/joint_trajectory (trajectory_msgs/msg/JointTrajectory)
  - joint_names: ["joint1", "joint2", "joint3", "joint4"]
  - points[0].positions: target joint angles in radians (float64[])
  - points[0].velocities, accelerations, effort: [] (empty)
  - points[0].time_from_start: builtin_interfaces/msg/Duration
- Serial Protocol (115200 baud): JOINTS:joint1=<deg>,joint2=<deg>,joint3=<deg>,joint4=<deg>\n (clamped to [0.0, 180.0] degrees)

## Pin Mapping (Common Ground Required)
| Joint / Signal | Microcontroller Pin | Notes |
| :--- | :--- | :--- |
| joint1 PWM | Pin 3 | Servo signal pin |
| joint2 PWM | Pin 5 | Servo signal pin |
| joint3 PWM | Pin 6 | Servo signal pin |
| joint4 PWM | Pin 9 | Servo signal pin |
| Ground (GND) | Shared GND | Tie MCU GND, external servo PSU GND, and servo ground together |
