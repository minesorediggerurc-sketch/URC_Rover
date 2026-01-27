import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command  # <--- NEW IMPORT
from launch_ros.actions import Node
from os.path import join

def generate_launch_description():
    # 1. Package Paths
    pkg_ros_ign_gazebo = get_package_share_directory('ros_ign_gazebo')
    pkg_ros_gz_rbot = get_package_share_directory('ROS_description')

    # 2. File Paths
    # Note: We do NOT process the file here anymore. We just point to it.
    robot_description_file = os.path.join(pkg_ros_gz_rbot, 'urdf', 'ROS.xacro')
    ros_gz_bridge_config = os.path.join(pkg_ros_gz_rbot, 'config', 'ros_gz_bridge_gazebo.yaml')
    rviz_config_file = os.path.join(pkg_ros_gz_rbot, 'config', 'rover_view.rviz')

    # 3. Process URDF using 'Command' (The Robust Way)
    # This runs "xacro <path/to/file>" in the shell and captures the output
    robot_description = {
        'robot_description': Command(['xacro ', robot_description_file])
    }

    # 4. Nodes
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description], # Passes the processed XML
    )
    
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            join(pkg_ros_ign_gazebo, "launch", "ign_gazebo.launch.py")
        ),
        launch_arguments={"ign_args": "-r -v 4 dem_moon.sdf"}.items()
    )

    spawn_robot = TimerAction(
        period=2.0,  # Increased timer slightly to ensure Gazebo is ready
        actions=[Node(
            package='ros_ign_gazebo',
            executable='create',
            arguments=[
                "-topic", "/robot_description",
                "-name", "ROS",
                "-allow_renaming", "false",
                "-x", "0.0",
                "-y", "0.0",
                "-z", "0.32",
                "-Y", "0.0"
            ],
            output='screen'
        )]
    )

    ros_gz_bridge = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': ros_gz_bridge_config}],
        output='screen'
    )
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        spawn_robot,
        ros_gz_bridge,
        robot_state_publisher,
        rviz_node,
    ])