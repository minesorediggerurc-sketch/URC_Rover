Gazebo: 
```
cd ros_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch ROS_description gazebo.launch.py

```
Controller:
New terminal:
```
cd ros_ws
colcon build --symlink-install
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

```
RViz:
(if you want the real cameras)
```
cd ros_ws
colcon build --symlink-install
source install/setup.bash
cd src
cd OrbbecSDK_ROS2
ros2 launch orbbec_camera gemini_330_series.launch.py enable_colored_point_cloud:=true

```
New Terminal: 
```
cd ros_ws
colcon build --symlink-install
ros2 run rviz2 rviz2
```
