#### Gazebo: 
```
cd ros_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch ROS_description gazebo.launch.py

```
The rover currently spawns inside the box on the shapes world.  To fix this, you can modify the pose (position) of the box or the rover so they don't overlap, or right click on the box and select remove.
#### Controller:
New terminal:
```
cd ros_ws
colcon build --symlink-install
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```


#### RViz:
(if you don't want the real cameras you can skip this part)
```
cd ros_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch orbbec_camera gemini_330_series.launch.py enable_colored_point_cloud:=true

```
New Terminal: 
```
cd ros_ws
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

CMake Error at CMakeLists.txt:26 (find_package):
  By not providing "FindPangolin.cmake" in CMAKE_MODULE_PATH this project has
  asked CMake to find a package configuration file provided by "Pangolin",
  but CMake did not find one.

  Could not find a package configuration file provided by "Pangolin" with any
  of the following names:

    PangolinConfig.cmake
    pangolin-config.cmake

  Add the installation prefix of "Pangolin" to CMAKE_PREFIX_PATH or set
  "Pangolin_DIR" to a directory containing one of the above files.  If
  "Pangolin" provides a separate development package or SDK, be sure it has
  been installed.




