"""Gazebo 시뮬레이션: 버거를 turtlebot3_world에 스폰 (use_sim_time:=True)."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    gz = get_package_share_directory('turtlebot3_gazebo')
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gz, 'launch', 'turtlebot3_world.launch.py')),
            launch_arguments={'use_sim_time': 'True'}.items()),
    ])
