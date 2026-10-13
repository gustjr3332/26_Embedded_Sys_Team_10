"""Nav2 자율주행. map 기본값은 패키지의 maps/map.yaml. 시뮬 기본값, 실물은 use_sim_time:=False."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    default_map = os.path.join(get_package_share_directory('tb3_team10'), 'maps', 'map.yaml')
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='True',
                              description='시뮬레이션 True, 실물 False'),
        DeclareLaunchArgument('map', default_value=default_map),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('turtlebot3_navigation2'), 'launch', 'navigation2.launch.py')),
            launch_arguments={'map': LaunchConfiguration('map'), 'use_sim_time': use_sim_time}.items()),
    ])
