# source scripts/env.sh  (2분반 2-10조: ROS_DOMAIN_ID=25, 파이와 같은 값이어야 함)
source /opt/ros/jazzy/setup.bash
[ -f "$(dirname "$BASH_SOURCE")/../install/setup.bash" ] && source "$(dirname "$BASH_SOURCE")/../install/setup.bash"
export TURTLEBOT3_MODEL=burger
export LDS_MODEL=LDS-02
export ROS_DOMAIN_ID=25
# Cyclone DDS가 설치된 뒤에만 적용 (sudo apt install ros-jazzy-rmw-cyclonedds-cpp)
if [ -d /opt/ros/jazzy/share/rmw_cyclonedds_cpp ]; then
  export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
  export CYCLONEDDS_URI="file://$(cd "$(dirname "$BASH_SOURCE")" && pwd)/cyclonedds.xml"
fi
