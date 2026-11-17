"""Nav2 자율주행. map 기본값은 패키지의 maps/map.yaml, 파라미터는 config/burger.yaml(튜닝 제출본). 시뮬 기본값, 실물은 use_sim_time:=False."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    pkg = get_package_share_directory('tb3_team10')
    default_map = os.path.join(pkg, 'maps', 'map.yaml')
    default_params = os.path.join(pkg, 'config', 'burger.yaml')
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='True',
                              description='시뮬레이션 True, 실물 False'),
        DeclareLaunchArgument('map', default_value=default_map),
        DeclareLaunchArgument('params_file', default_value=default_params),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('turtlebot3_navigation2'), 'launch', 'navigation2.launch.py')),
            launch_arguments={'map': LaunchConfiguration('map'), 'use_sim_time': use_sim_time,
                              'params_file': LaunchConfiguration('params_file')}.items()),
    ])
