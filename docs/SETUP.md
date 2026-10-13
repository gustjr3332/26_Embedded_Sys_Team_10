# TurtleBot3 Burger 환경 구축 진행표

ROS 2 Jazzy · Ubuntu 24.04 (WSL2) 기준. 절차 원본: `src/26_2_Embeded_System/TurtleBot3_Burger_조립_SLAM_Nav2_실습_매뉴얼.pdf`

마지막 갱신: 2026-10-12

## 1. 현재 상태 (2026-10-12 점검)

| 항목 | 상태 |
|---|---|
| ROS 2 Jazzy (`ros-jazzy-desktop`) | ✅ 설치됨 |
| Node.js 18 (Claude Code 훅용) | ✅ 설치됨 |
| TurtleBot3 패키지 | ✅ 설치됨 (apt) |
| Gazebo Harmonic / ros_gz | ✅ 설치됨 |
| Cartographer / Nav2 | ✅ 설치됨 |
| 환경변수 (`ROS_DOMAIN_ID`, `TURTLEBOT3_MODEL`) | ✅ `~/.bashrc`에 설정 |
| WSL 네트워크 | ⚠️ NAT 모드 → 라즈베리파이와 DDS 통신 불가 |
| 워크스페이스 코드 | ⚠️ `my_cpp_pkg/src/my_code.cpp`(타이머 노드)만 소스 있음. 나머지 패키지는 껍데기 |

## 2. 설치할 패키지

### Remote PC (이 WSL)

```bash
# TurtleBot3 본체 + 메시지
sudo apt install -y ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-msgs

# Gazebo 시뮬레이션 (Gazebo Harmonic 같이 설치됨)
sudo apt install -y ros-jazzy-ros-gz ros-jazzy-turtlebot3-gazebo

# SLAM
sudo apt install -y ros-jazzy-cartographer ros-jazzy-cartographer-ros

# 자율주행
sudo apt install -y ros-jazzy-navigation2 ros-jazzy-nav2-bringup
```

선택: `poppler-utils` (PDF를 터미널에서 읽기)

### SBC (라즈베리파이 4, Ubuntu Server 24.04)

```bash
sudo apt install -y ros-jazzy-ros-base python3-colcon-common-extensions \
  ros-jazzy-hls-lfcd-lds-driver ros-jazzy-turtlebot3-msgs \
  ros-jazzy-dynamixel-sdk ros-jazzy-xacro libudev-dev
# 이후 turtlebot3, ld08_driver, coin_d4_driver를 jazzy 브랜치로 clone 후
# colcon build --parallel-workers 1  (매뉴얼 3.3절)
```

## 3. 환경 설정

`~/.bashrc`에 추가 (Remote PC·SBC 값이 같아야 함):

```bash
export ROS_DOMAIN_ID=30
export TURTLEBOT3_MODEL=burger
export LDS_MODEL=LDS-02        # SBC만
```

실물 연동 전 Windows `C:\Users\gustj\.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
```

→ `wsl --shutdown` 후 재시작. 안 되면 Windows 방화벽 UDP 허용 확인.

## 4. 진행 체크리스트

### Claude Code 환경
- [x] 프로젝트 전용 `~/workspace/CLAUDE.md` 작성 (Windows CLAUDE.md import)
- [x] scout/builder 에이전트 연결 (`~/workspace/.claude/agents/` → Windows 심볼릭 링크)
- [x] ADHD 모드 always-on (`~/.claude/.i-have-adhd-always`)
- [x] ponytail 설치, 프로젝트 범위로 활성화
- [x] Node.js 설치 → 두 SessionStart 훅 직접 실행해 동작 확인

### 시뮬레이션 (Gazebo)
- [x] 2장 Remote PC 패키지 설치
- [x] 3장 환경변수 설정
- [x] `ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py` 실행 확인 (GUI segfault → `LIBGL_ALWAYS_SOFTWARE=1 GZ_IP=127.0.0.1`로 해결)
- [ ] `ros2 run turtlebot3_teleop teleop_keyboard`로 직접 조작 (미확인)
- [x] Cartographer SLAM → 지도 저장 `~/workspace/map.pgm/.yaml` (키보드 대신 `~/workspace/wander.py` 자동 주행으로 생성)
- [x] Nav2 자율주행: 초기 위치 지정 후 목표 `(-0.5, 0.5)` 도착 확인

지도 재현: Gazebo → `cartographer.launch.py use_sim_time:=True` → `python3 ~/workspace/wander.py 300` → `map_saver_cli -f ~/workspace/map`

### 실물 로봇
- [ ] 하드웨어 조립 (ROBOTIS 공식 PDF)
- [ ] 라즈베리파이 SD 카드에 Ubuntu Server 24.04 설치, Wi-Fi·SSH 설정
- [ ] SBC 패키지 설치·빌드, udev 규칙, `LDS_MODEL`
- [ ] OpenCR 펌웨어 업로드 → SW1(전진 30cm)/SW2(180° 회전) 테스트
- [ ] WSL mirrored 모드 전환
- [ ] Bringup → PC에서 `ros2 topic list`로 `/scan`, `/odom` 보이는지 확인
- [ ] 텔레옵 → SLAM → Nav2

## 5. 주의사항
- Jazzy부터 `/cmd_vel` 타입은 `TwistStamped`. 직접 짠 퍼블리셔도 맞춰야 함.
- 시뮬레이션에서는 모든 launch에 `use_sim_time:=True`.
- Gazebo에서 재현 안 되는 것: 배터리 상태, OpenCR 버튼/사운드, 실제 노이즈·바퀴 슬립, PC↔SBC 네트워크.
- Nav2 실행 중에는 텔레옵을 끌 것 (`/cmd_vel` 충돌).
