# 26 임베디드시스템 10조 — TurtleBot3 Burger

ROS 2 Jazzy · WSL2 Ubuntu 24.04 · TurtleBot3 Burger (Gazebo Harmonic)

## 시작
먼저 ROS 2 Jazzy(`ros-jazzy-desktop`)가 있어야 한다. 그다음 TurtleBot3 패키지를 설치한다.
```bash
sudo apt install -y ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-msgs ros-jazzy-ros-gz ros-jazzy-turtlebot3-gazebo ros-jazzy-turtlebot3-cartographer ros-jazzy-turtlebot3-navigation2
```
그 뒤 레포를 받아 빌드한다.
```bash
git clone https://github.com/gustjr3332/26_Embedded_Sys_Team_10.git ~/tb3 && cd ~/tb3
source scripts/env.sh
colcon build && source install/setup.bash
ros2 launch tb3_team10 sim.launch.py   # Gazebo 시뮬레이션
```

## SLAM과 Nav2
터미널마다 `source scripts/env.sh`를 먼저 실행한다. 실물 로봇이면 `use_sim_time:=False`를 붙인다.
```bash
ros2 launch tb3_team10 sim.launch.py     # 1) 시뮬레이션
ros2 launch tb3_team10 slam.launch.py    # 2) SLAM (텔레옵 `ros2 run turtlebot3_teleop teleop_keyboard`로 지도 작성)
ros2 run nav2_map_server map_saver_cli -f ~/map   # 3) 지도 저장
ros2 launch tb3_team10 nav.launch.py     # 4) Nav2 (기본 지도: 패키지의 maps/map.yaml)
ros2 launch tb3_team10 nav.launch.py map:=$HOME/map.yaml   # 내 지도로 실행
```
SLAM과 Nav2는 동시에 켜지 않는다. 팀 지도는 `src/tb3_team10/maps/`에 넣는다.
- 진행 상황·설치 체크리스트: [docs/SETUP.md](docs/SETUP.md)
- 지도: `src/tb3_team10/maps/`
- AI 에이전트 규칙: [docs/AI_AGENT_RULES.md](docs/AI_AGENT_RULES.md)

## 협업 규칙
- `main` 직접 push 금지. `feat/이름-내용` 브랜치 → PR → 상대 승인 후 merge.
- 강의 PDF·비밀번호·Wi-Fi 정보는 올리지 않는다 (public 레포).
