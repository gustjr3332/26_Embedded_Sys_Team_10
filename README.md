# 26 임베디드시스템 10조 TurtleBot3 Burger

ROS 2 Jazzy, WSL2 Ubuntu 24.04, TurtleBot3 Burger, Gazebo Harmonic

## 설치
ROS 2 Jazzy(`ros-jazzy-desktop`)를 먼저 설치하고, 그다음 TurtleBot3 패키지를 설치한다.
```bash
sudo apt install -y ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-msgs ros-jazzy-ros-gz ros-jazzy-turtlebot3-gazebo ros-jazzy-turtlebot3-cartographer ros-jazzy-turtlebot3-navigation2
```
레포를 받아 빌드한다.
```bash
git clone https://github.com/gustjr3332/26_Embedded_Sys_Team_10.git ~/tb3 && cd ~/tb3
source scripts/env.sh
colcon build && source install/setup.bash
```

## 시뮬레이션에서 SLAM으로 지도 만들기
새 터미널을 열 때마다 `cd ~/tb3 && source scripts/env.sh`부터 실행한다.

터미널 1에서 Gazebo를 띄운다. turtlebot3_world에 버거가 나타나면 된다.
```bash
cd ~/tb3 && source scripts/env.sh
LIBGL_ALWAYS_SOFTWARE=1 GZ_IP=127.0.0.1 ros2 launch tb3_team10 sim.launch.py
```
앞의 두 환경변수는 WSL2에서 Gazebo GUI가 segfault로 죽는 문제를 피하려고 넣었다. 일반 Ubuntu에서는 빼도 된다.

터미널 2에서 Cartographer SLAM을 실행한다. RViz가 뜨고 라이다 스캔으로 지도가 그려지기 시작한다.
```bash
cd ~/tb3 && source scripts/env.sh
ros2 launch tb3_team10 slam.launch.py
```

지도를 채우려면 로봇을 움직여야 한다. 터미널 3에서 키보드로 조종하거나(`w`/`x` 전진·후진, `a`/`d` 회전, `s` 정지) 자동 주행 스크립트를 돌린다.
```bash
cd ~/tb3 && source scripts/env.sh
ros2 run turtlebot3_teleop teleop_keyboard
# 또는 300초 동안 장애물을 피하며 돌아다니기
python3 scripts/wander.py 300
```

RViz에서 벽이 빈틈없이 이어지면 같은 터미널에서 지도를 저장한다. `~/map.pgm`과 `~/map.yaml`이 생긴다.
```bash
ros2 run nav2_map_server map_saver_cli -f ~/map
```
팀에서 같이 쓸 지도는 `src/tb3_team10/maps/`에 복사한다.

실물 로봇에서는 터미널 1 대신 SBC에서 `ros2 launch tb3_team10 robot.launch.py`를 실행하고, SLAM에 `use_sim_time:=False`를 붙인다.

## Nav2 자율주행
SLAM을 끈 뒤 실행한다. 둘을 동시에 켜지 않는다.
```bash
ros2 launch tb3_team10 nav.launch.py                        # 패키지의 maps/map.yaml 사용
ros2 launch tb3_team10 nav.launch.py map:=$HOME/map.yaml    # 직접 만든 지도 사용
```
RViz에서 2D Pose Estimate로 초기 위치를 찍고 Nav2 Goal로 목표를 찍는다. Nav2가 도는 동안 텔레옵은 끈다(`/cmd_vel` 충돌).

## 문서
- 진행 상황과 설치 체크리스트: [docs/SETUP.md](docs/SETUP.md)
- AI 에이전트 규칙: [docs/AI_AGENT_RULES.md](docs/AI_AGENT_RULES.md)

## 협업 규칙
- `main`에 직접 push하지 않는다. `feat/이름-내용` 브랜치를 만들어 PR을 올리고, 상대가 승인하면 merge한다.
- 강의 PDF, 비밀번호, Wi-Fi 정보는 올리지 않는다(public 레포).
