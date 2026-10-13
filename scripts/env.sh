# source scripts/env.sh  (팀원마다 ROS_DOMAIN_ID를 다르게: A=30, B=31. 로봇 쓸 때만 30으로 맞춤)
source /opt/ros/jazzy/setup.bash
[ -f "$(dirname "$BASH_SOURCE")/../install/setup.bash" ] && source "$(dirname "$BASH_SOURCE")/../install/setup.bash"
export TURTLEBOT3_MODEL=burger
export LDS_MODEL=LDS-02
export ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-30}
