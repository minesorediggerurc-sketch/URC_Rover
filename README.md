#### Gazebo: 
```
cd ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch ROS_description gazebo.launch.py

```
The rover currently spawns inside the box on the shapes world.  To fix this, you can modify the pose (position) of the box or the rover so they don't overlap, or right click on the box and select remove.
#### Controller:
New terminal:
```
cd ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```


#### RViz:
(if you don't want the real cameras you can skip this part)
```
cd ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch orbbec_camera gemini_330_series.launch.py enable_colored_point_cloud:=true

```
New Terminal: 
```
cd ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 run rviz2 rviz2
```
Under Fixed Frame choose base_link. Click add at the bottom left, scroll down and choose RobotModel.  In RobotModel, click next to Description Topic (it is secretly a dropdown) and select /robot_description to see the rover.  To see the camera feed, click add, and then By topic at the top.  Then select camera/depth_registered/points/PointCloud2 to see the depth camera out of the orbbec.  If you just want to see the gazebo simulated pointcloud, go to add By topic and pick depth_camera/points/PointCloud2.
#### Orbbec viewer:
```
cd Downloads/OrbbecViewer_v1.10.27_202509260950_arm64_release
sudo ./OrbbecViewer
```
Password is 'password'.
Make sure camera is plugged in.  Select the cammera from the dropdown on top left if not already done.  Select which view you want (color, depth, ir left, ir right, imu, pointcloud).

```
ros2 launch orbbec_camera gemini_330_series.launch.py \
    depth_width:=640 depth_height:=480 depth_fps:=30 \
    color_width:=640 color_height:=480 color_fps:=30 \
    enable_colored_point_cloud:=true
```
To create start OrbSlam and display point cloud through RViz complete the following:

In first terminal tab:
```
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch orbbec_camera gemini_330_series.launch.py \
    depth_width:=640 depth_height:=480 depth_fps:=30 \
    color_width:=640 color_height:=480 color_fps:=30 \
    enable_colored_point_cloud:=true
```

In a new terminal tab:
```
cd ~/ros2_ws
colcon build --symlink-install --packages-select orbslam3
source install/setup.bash
ros2 run orbslam3 rgbd     ~/ros2_ws/src/orbslam3_ros2/vocabulary/ORBvoc.txt     ~/ros2_ws/src/orbslam3_ros2/config/rgb-d/Orbbec_Gemini335.yaml     --ros-args     -r camera/rgb:=/camera/color/image_raw     -r camera/depth:=/camera/depth/image_raw
```

In a new terminal tab:
```
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
ros2 run rviz2 rviz2
```

After all of this, you should be able to add "TF", "Pose", and "PointCloud2 - topic of orbslam" to be able to see OrbSlam within RViz

This is the start of Nav2 Stuff (Updated when finished; everything in cd ros_ws unless otherwise specified)
After doing all the previous terminals for ORB_SLAM3, do the next steps

New Terminal Tab:
```
ros2 run robot_localization ekf_node --ros-args --params-file ~/ros2_ws/src/my_robot_bringup/config/ekf2.yaml
```

New Terminal Tab:
```
ros2 run depthimage_to_laserscan depthimage_to_laserscan_node --ros-args -r /depth:=/camera/depth/image_raw -r /depth_camera_info:=/camera/depth/camera_info
```

New Terminal Tab:
```
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 camera_link base_link
```

New Terminal Tab:
```
ros2 launch nav2_bringup navigation_launch.py \
  params_file:=/home/urc/ros2_ws/src/my_robot_bringup/params/nav2_params.yaml \
  use_sim_time:=False
```
