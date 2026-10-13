"""실물 버거 bringup (SBC에서 실행). ROS_DOMAIN_ID, LDS_MODEL은 scripts/env.sh로 설정."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    bringup = get_package_share_directory('turtlebot3_bringup')
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(bringup, 'launch', 'robot.launch.py'))),
    ])
