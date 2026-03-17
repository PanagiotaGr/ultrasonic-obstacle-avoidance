# Ultrasonic Obstacle Avoidance

This project presents the development and experimental evaluation of a reactive obstacle avoidance algorithm for a mobile robot using ultrasonic sensors. Due to the inherent noise and uncertainty in ultrasonic measurements, the study investigates the impact of filtering techniques and parameter tuning on navigation performance. A baseline rule-based controller is compared with an improved version incorporating median filtering and directional correction. Experimental results across multiple scenarios demonstrate that the enhanced controller significantly reduces collision rates and improves motion smoothness. The findings highlight the importance of sensor data preprocessing and parameter optimization in robust robot navigation systems.

Development and optimization of an obstacle avoidance algorithm for a mobile robot using ultrasonic sensors in ROS 2 Jazzy on Ubuntu 24.04.

## Overview

This project implements a reactive obstacle avoidance controller for a mobile robot using three ultrasonic distance sensors:

- left sensor
- front sensor
- right sensor

The algorithm processes sensor measurements, applies filtering to reduce noise, and publishes motion commands based on obstacle proximity.

## Features

- ROS 2 Jazzy Python package
- Reactive obstacle avoidance logic
- Median filtering for ultrasonic sensor measurements
- Velocity command generation through `/cmd_vel`
- Easy testing with manually published sensor values
- Suitable as a university robotics project foundation

## System Architecture

The system is divided into three layers:

1. **Sensor input layer**  
   Receives ultrasonic distance measurements from ROS 2 topics.

2. **Filtering layer**  
   Applies median filtering to reduce outliers and unstable readings.

3. **Control layer**  
   Computes linear and angular velocity commands for obstacle avoidance.

## Topics

### Subscribed Topics

- `/ultra_left` (`std_msgs/msg/Float32`)
- `/ultra_front` (`std_msgs/msg/Float32`)
- `/ultra_right` (`std_msgs/msg/Float32`)

### Published Topics

- `/cmd_vel` (`geometry_msgs/msg/Twist`)

## Control Logic

The controller follows a reactive rule-based strategy:

- If the front distance is below the stop threshold, the robot stops and turns toward the safer side.
- If the front distance is below the safe threshold, the robot slows down and turns away from the obstacle.
- If the path is clear, the robot moves forward while applying a side correction term based on left-right distance difference.

## Parameters in Current Implementation

Main parameters currently defined in code:

- `safe_distance`
- `stop_distance`
- `max_linear_speed`
- `max_angular_speed`
- `side_gain`

## Requirements

- Ubuntu 24.04
- ROS 2 Jazzy
- Python 3
- colcon

## Build

```bash
source /opt/ros/jazzy/setup.bash
cd ~/robot_ws
colcon build
source install/setup.bash
