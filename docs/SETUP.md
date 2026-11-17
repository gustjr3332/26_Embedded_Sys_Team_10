# TurtleBot3 Burger 조립·개발 계획

이 팀은 TurtleBot3 Burger 한 대만 다룬다. 기준 환경은 아래와 같고 Remote PC와 SBC 값이 같아야 한다.

| 항목 | 값 |
|---|---|
| 로봇 | TurtleBot3 Burger (`TURTLEBOT3_MODEL=burger`) |
| 라이다 | LDS-02 (`LDS_MODEL=LDS-02`, SBC에서 설정) |
| 제어 보드 | OpenCR 1.0, DYNAMIXEL XL430 2개 |
| SBC | Raspberry Pi 4, Ubuntu Server 24.04 LTS 64-bit, ROS 2 Jazzy ros-base |
| Remote PC | WSL2 Ubuntu 24.04, ROS 2 Jazzy desktop |
| 네트워크 | `ROS_DOMAIN_ID=25`, `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp` |
| 속도 명령 | `/cmd_vel`은 `geometry_msgs/TwistStamped` (Jazzy부터) |

참고 자료
- ROBOTIS e-Manual: https://docs.robotis.com/docs/systems/turtlebot3/overview/
- Burger 조립 매뉴얼 PDF (ROBOTIS 배포): http://www.robotis.com/service/download.php?no=748
- 로컬 사본: `~/workspace/src/26_2_Embeded_System/` 안의 `TURTLEBOT3_QS_BURGER_VER2544(online).pdf`(공식 Quick Start, 2025-09 Rev.10)와 `TurtleBot3_Burger_조립_SLAM_Nav2_실습_매뉴얼.pdf`(수업 매뉴얼). 저작권 때문에 이 레포에는 넣지 않는다.

마지막 갱신: 2026-10-13

## 1. 현재 상태 (2026-10-12 점검)

| 항목 | 상태 |
|---|---|
| ROS 2 Jazzy (`ros-jazzy-desktop`) | 설치됨 |
| Node.js 18 (Claude Code 훅용) | 설치됨 |
| TurtleBot3 패키지 | 설치됨 (apt) |
| Gazebo Harmonic / ros_gz | 설치됨 |
| Cartographer / Nav2 | 설치됨 |
| 환경변수 (`ROS_DOMAIN_ID`, `TURTLEBOT3_MODEL`) | `~/.bashrc`에 설정됨 |
| WSL 네트워크 | 주의: NAT 모드라 라즈베리파이와 DDS 통신 불가 |
| 팀 패키지 | `src/tb3_team10`(ament_cmake): `sim.launch.py`, `robot.launch.py`. 빌드 확인, 시뮬 실행은 미확인 |
| 수업 실습 패키지 | `~/workspace/src`의 `my_*` 등. 레포에 넣지 않음 |

---

# A. 조립 계획

순서는 부품 확인, 기구 조립(1층부터 4층), 배선 점검, 배터리 준비, SBC 설치, OpenCR 펌웨어 업로드, SW1/SW2 테스트다. 조립 중에는 공식 PDF 그림을 옆에 펴 두고 나사 규격을 하나씩 맞춰 본다.

## A1. 부품 확인

상자를 열면 공식 PDF 마지막의 Parts List와 대조한다. 큰 부품만 먼저 센다.

- DYNAMIXEL XL430 2개, DYNAMIXEL to OpenCR 케이블 2개
- OpenCR 1.0 1개, Raspberry Pi 1개, USB2LDS 보드 1개, 360 Laser Distance Sensor(LDS-02, LD08) 1개와 LDS 케이블
- USB 케이블 2개, Raspberry Pi 전원 케이블 1개, Li-Po 배터리 연장 케이블 1개
- Li-Po 배터리, 충전기 LBC-010, SMPS(12V 어댑터), AC 코드
- Waffle-Plate 8장, 바퀴와 타이어 각 2개, 볼 캐스터 1개, 브래킷 5개
- Plate_Support M3×35mm 4개, M3×45mm 10개, PCB Support 12개, Spacer, Adapter Plate, 리벳

나사와 너트는 종류가 많고 생김새가 비슷하다. PDF 마지막 장에 1:1 크기 도안이 있으니 헷갈리면 그 위에 대 본다. 공구는 키트에 든 드라이버와 리벳 도구만 쓴다.

## A2. 조립 순서

공식 PDF의 Assembly Manual(9~26쪽) 그림 순서와 같다. 로봇은 4개 층을 위로 쌓아 만든다. 한 층은 Waffle-Plate 2장을 겹친 것이다.

| 층 | 들어가는 것 |
|---|---|
| 1층 | 바퀴 모터(DYNAMIXEL) 2개, 바퀴, 배터리, 볼 캐스터 |
| 2층 | OpenCR(모터를 움직이는 제어 보드) |
| 3층 | 라즈베리파이(로봇의 컴퓨터), USB2LDS |
| 4층 | LDS-02(주변 거리를 재는 센서) |

이름이 낯선 부품은 이렇게 부른다.

| 이름 | 쉬운 설명 |
|---|---|
| Waffle-Plate | 구멍이 촘촘히 뚫린 판. 한 층에 2장씩 쓴다 |
| Plate_Support | 층과 층 사이를 받치는 기둥 (1층은 35mm, 나머지는 45mm) |
| PCB Support | 보드를 판에서 띄워 주는 작은 받침 |
| Rivet | 누르면 박히는 플라스틱 못. 나사 대신 쓴다 |
| Cable Passage | 판에 난 케이블 통로. 층을 얹기 전에 케이블을 먼저 빼 둔다 |

### 시작 전에

1. 층마다 부품 목록 그림이 나온다. 그 층 부품만 꺼내 따로 놓고 시작한다.
2. 나사 이름은 `PH_M3×8mm_K`처럼 "모양_굵기×길이"다. 굵기(M2, M2.5, M3)와 길이를 PDF 그림과 맞춰 본다. 헷갈리면 PDF 마지막 장의 1:1 도안에 대 본다.
3. Waffle-Plate 2장을 겹쳐 한 층으로 만든다. 이때 쓰는 나사는 `PH_M3×8mm_K`, 너트는 `NUT_M3`다.
   - 1, 3, 4층은 나사를 판 위쪽에서 넣는다.
   - 2층만 나사를 판 아래쪽에서 넣는다. 나사 끝이 배터리를 긁지 않게 하려는 것이다.

### 1층: 바퀴와 배터리

이 층 부품: M2×4mm 8개, T2×6mm 4개, T2.6×12mm 8개, M3×8mm 8개, 너트 M3 4개, Plate_Support 35mm 4개, 브래킷 5개, 리벳 10개.

1. 볼 캐스터(앞뒤 균형을 잡는 작은 바퀴)를 1층 판의 아래쪽에 달고 `PH_T2×6mm_K`로 고정한다.
2. Plate_Support 35mm 4개를 `PH_M3×8mm_K`로 판에 세운다.
3. 타이어를 바퀴에 끼운다.
4. 바퀴를 DYNAMIXEL에 `PH_M2×4mm_K`로 고정한다.
5. 직각 브래킷으로 배터리 자리를 만든다. 배터리가 흔들리지 않게 잡아 주는 틀이다.
6. DYNAMIXEL 2개를 1층 판에 올리고 DYNAMIXEL to OpenCR 케이블을 각각 꽂는다.
   - PDF 그림의 ID 1, ID 2 위치와 바퀴 방향을 그대로 맞춘다. 좌우가 바뀌면 SW1 테스트에서 로봇이 엉뚱하게 돈다.
7. Li-Po 배터리를 두 DYNAMIXEL 사이에 놓는다.

### 2층: OpenCR

이 층 부품: PCB Support 4개, M2.5×8mm 4개, M3×8mm 12개, 너트 M2.5 4개, 너트 M3 4개, T2.6×12mm 8개, Plate_Support 45mm 4개, 리벳 4개, 배터리 연장 케이블 1개.

1. 1층에서 꽂은 DYNAMIXEL 케이블 2개를 2층 판의 케이블 통로로 먼저 뺀다. PCB Support를 단 뒤에는 빼기 어렵다.
2. OpenCR용 PCB Support 4개를 판에 단다. PDF가 권하는 나사 위치 그림을 따른다.
3. OpenCR을 PCB Support 위에 올린다.
4. Plate_Support 45mm 4개를 세우고 2층을 1층 위에 얹는다.
5. 2층 위쪽에서 `PH_T2.6×12mm_K`로 DYNAMIXEL을 고정한다.

### 3층: 라즈베리파이

이 층 부품: PCB Support 4개, M2.5×8mm 8개, M3×8mm 14개, 너트 M2.5 8개, 너트 M3 4개, Plate_Support 45mm 6개, 리벳 2개, USB 케이블 2개, 라즈베리파이 전원 케이블 1개, USB2LDS 1개, Adapter Plate 1개.

1. 너트 M2.5를 라즈베리파이용 PCB Support의 홈에 끼운다.
2. USB 케이블과 라즈베리파이 전원 케이블을 각자 맞는 통로로 먼저 뺀다.
3. PCB Support 위치를 맞춰 판에 단다.
4. 라즈베리파이를 PCB Support 위에 올린다.
5. USB2LDS와 Adapter Plate를 리벳으로 판에 고정한다.
6. 케이블을 꽂는다.
   - OpenCR과 라즈베리파이를 USB 케이블로 잇는다.
   - 라즈베리파이 전원 케이블을 라즈베리파이 GPIO에 꽂는다. PIN 4가 +, PIN 6이 −다. 거꾸로 꽂으면 안 된다.
   - 라즈베리파이와 USB2LDS를 USB 케이블로 잇는다.
7. 3층을 2층 위에 얹는다.

### 4층: LDS-02

이 층 부품: PCB Support 3개, M2.5×8mm 3개, M2.5×16mm 3개, M3×8mm 10개, 너트 M2.5 6개, 너트 M3 4개, Spacer 3개, LDS 케이블 1개.

1. 너트 M2.5를 LDS용 PCB Support의 홈에 끼운다.
2. LDS 케이블을 통로로 먼저 뺀다.
3. PCB Support 위치를 맞춰 판에 단다.
4. PCB Support 위에 Spacer를 놓고, 그 위에 LDS를 `PH_M2.5×16mm_K`로 올려 고정한다.
5. 4층을 3층 위에 얹는다.
6. LDS 케이블을 3층의 USB2LDS에 꽂는다.

### 끝나고 확인

- 나사나 부품이 남지 않았는가. 층마다 남은 개수가 있으면 어디선가 빠진 것이다.
- 바퀴 좌우(ID 1, ID 2)가 PDF 그림과 같은가.
- 케이블이 바퀴나 판 사이에 끼지 않았는가.
- 라즈베리파이 전원 케이블이 PIN 4(+), PIN 6(−)에 맞는가.

배선 확인은 A3, 배터리 준비는 A4로 이어진다.

## A3. 배선

| 연결 | 케이블 | 확인할 점 |
|---|---|---|
| DYNAMIXEL ID1, ID2 ↔ OpenCR | DYNAMIXEL to OpenCR | 커넥터 모양과 방향 |
| OpenCR ↔ 라즈베리파이 | USB | 펌웨어 업로드와 bringup 모두 이 선으로 한다 |
| OpenCR ↔ 라즈베리파이 GPIO | 라즈베리파이 전원 케이블 | PIN 4가 +, PIN 6이 −. 거꾸로 꽂으면 안 된다 |
| 라즈베리파이 ↔ USB2LDS | USB | |
| USB2LDS ↔ LDS-02 | LDS 케이블 | |
| 배터리 ↔ OpenCR | 배터리 연장 케이블 | |

케이블을 뺄 때는 선이 아니라 커넥터를 잡고 당긴다.

## A4. 배터리와 전원

- 배터리에는 로봇용과 충전용 커넥터가 따로 있다. 충전은 SMPS에 LBC-010 충전기를 물리고 충전용 커넥터를 꽂으면 바로 시작된다. LED가 빨강이면 충전 중, 초록이면 완료다.
- 주행 중 저전압 경고음이 나면 즉시 배터리를 빼서 충전한다.
- SMPS를 OpenCR 전원 잭에 직접 꽂으면 로봇을 켠 채로 배터리를 뺄 수 있다. SBC 빌드는 한 시간 넘게 걸릴 수 있으니 이때는 SMPS 전원을 쓴다.
- 책상 위에서 바퀴를 돌리지 않는다. 떨어져서 생긴 고장은 보증이 안 된다.

## A5. SBC(라즈베리파이) 설정

1. Raspberry Pi Imager로 microSD에 Ubuntu Server 24.04.2 LTS (64-bit)를 굽는다. Desktop이 아니라 Server 이미지다. Imager에서 Wi-Fi와 SSH를 미리 설정해 두면 모니터 없이 접속할 수 있다.
2. ROS 2 Jazzy 공식 Debian 설치 가이드대로 `ros-jazzy-ros-base`를 설치한다.
3. RAM 2GB 모델이면 빌드 전에 2GB 스왑을 만든다. 없으면 메모리 부족으로 빌드가 실패한다(명령은 e-Manual SBC Setup 참고).
4. 패키지 설치와 빌드:

```bash
sudo apt install -y python3-argcomplete python3-colcon-common-extensions libboost-system-dev build-essential
sudo apt install -y ros-jazzy-hls-lfcd-lds-driver ros-jazzy-turtlebot3-msgs \
  ros-jazzy-dynamixel-sdk ros-jazzy-xacro libudev-dev

mkdir -p ~/turtlebot3_ws/src && cd ~/turtlebot3_ws/src
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/ld08_driver.git
cd ~/turtlebot3_ws/src/turtlebot3 && rm -r turtlebot3_cartographer turtlebot3_navigation2
cd ~/turtlebot3_ws && colcon build --symlink-install --parallel-workers 1
```

5. OpenCR USB 포트용 udev 규칙:

```bash
sudo cp `ros2 pkg prefix turtlebot3_bringup`/share/turtlebot3_bringup/script/99-turtlebot3-cdc.rules /etc/udev/rules.d/
sudo sed -i 's/^ATTRS{idVendor}=="10c4"/KERNEL=="ttyUSB*", &/' /etc/udev/rules.d/99-turtlebot3-cdc.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

두 번째 줄은 `/dev/tb3_lidar`가 `ttyUSB0`가 아니라 `bus/usb/...`에 붙어서 라이다 포트가 안 열리는 문제를 막는다.

6. SBC `~/.bashrc`:

```bash
source /opt/ros/jazzy/setup.bash
source ~/turtlebot3_ws/install/setup.bash
export ROS_DOMAIN_ID=25 #TURTLEBOT3
export TURTLEBOT3_MODEL=burger
export LDS_MODEL=LDS-02
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

## A6. OpenCR 펌웨어 업로드

OpenCR과 라즈베리파이를 USB로 연결한 상태에서 SBC에서 실행한다.

```bash
sudo dpkg --add-architecture armhf
sudo apt-get update
sudo apt-get install libc6:armhf
export OPENCR_PORT=/dev/ttyACM0
export OPENCR_MODEL=burger
rm -rf ./opencr_update.tar.bz2
wget https://github.com/ROBOTIS-GIT/OpenCR-Binaries/raw/master/turtlebot3/ROS2/latest/opencr_update.tar.bz2
tar -xvf opencr_update.tar.bz2
cd ./opencr_update
./update.sh $OPENCR_PORT $OPENCR_MODEL.opencr
```

업로드가 실패하면 복구 모드로 들어가 다시 시도한다. PUSH SW2를 누른 채 Reset을 눌렀다 떼고, 그다음 SW2를 뗀다. 복구 모드에서는 STATUS LED가 깜빡인다.

## A7. SW1/SW2 점검

로봇을 바닥에 내려놓고 주변 1m 정도를 비운다. OpenCR 전원 스위치를 켜서 빨간 Power LED가 들어오는지 본다.

- PUSH SW1을 몇 초 누르고 있으면 30cm 전진해야 한다.
- PUSH SW2를 몇 초 누르고 있으면 제자리에서 180도 돌아야 한다.

둘 다 맞으면 DYNAMIXEL 좌우 설정과 펌웨어가 정상이다. 바퀴가 안 돌거나 방향이 틀리면 A2의 ID 위치부터 다시 보고, 그래도 안 되면 e-Manual FAQ의 DYNAMIXEL 설정 항목을 따른다.

---

# B. 개발 계획

## B1. Remote PC 준비

### 설치할 패키지

지금 이 WSL에는 TurtleBot3를 apt로 설치했고 시뮬레이션까지 이걸로 확인했다.

```bash
sudo apt install -y ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-msgs
sudo apt install -y ros-jazzy-ros-gz ros-jazzy-turtlebot3-gazebo
sudo apt install -y ros-jazzy-cartographer ros-jazzy-cartographer-ros
sudo apt install -y ros-jazzy-navigation2 ros-jazzy-nav2-bringup
```

e-Manual PC Setup은 TurtleBot3를 소스로 빌드하는 방식을 안내한다. 실물 연동에서 apt 버전과 SBC 쪽 jazzy 브랜치가 안 맞는 문제가 보이면 아래로 바꾼다.

```bash
mkdir -p ~/turtlebot3_ws/src && cd ~/turtlebot3_ws/src
git clone -b jazzy https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
cd ~/turtlebot3_ws && colcon build --symlink-install
echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc
```

### 환경 설정

`~/.bashrc`:

```bash
export ROS_DOMAIN_ID=25
export TURTLEBOT3_MODEL=burger
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

실물 연동 전 Windows `C:\Users\gustj\.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
```

`wsl --shutdown` 후 재시작한다. 그래도 안 보이면 Windows 방화벽의 UDP 허용을 확인한다. 공유기도 멀티캐스트를 지원해야 한다.

### 팀 패키지 tb3_team10

우리 launch와 이후 과제 코드는 레포 `src/tb3_team10`에 둔다. 공식 `turtlebot3*` 패키지는 복사하지 않고 apt 설치본을 include한다.

```bash
cd ~/tb3 && source scripts/env.sh
colcon build --packages-select tb3_team10 && source install/setup.bash
ros2 launch tb3_team10 sim.launch.py     # Gazebo 시뮬레이션
ros2 launch tb3_team10 robot.launch.py   # 실물 bringup, SBC에서 실행
```

노드나 params를 추가할 때는 이 패키지 안에서 늘린다. 패키지가 둘 이상 필요해지면 `tb3_team10_` 접두어로 나눈다.

## B2. 역할 분담

| 역할 | 담당 | 맡는 일 |
|---|---|---|
| 하드웨어·SBC | ______ | A 전체(조립, 배선, SBC 설치, 펌웨어, SW1/SW2), bringup 유지 |
| Remote PC·소프트웨어 | ______ | WSL 네트워크, SLAM과 Nav2 실행, 지도 관리, 팀 패키지 개발 |

조립(A2, A3)과 SLAM 주행은 두 명이 같이 한다. 한 사람은 PDF를 읽고 한 사람은 손을 움직이면 실수가 줄어든다.

## B3. 단계별 목표와 완료 기준

| 단계 | 목표 | 완료 기준 | 담당 |
|---|---|---|---|
| 0 시뮬레이션 | `ros2 launch tb3_team10 sim.launch.py`로 Gazebo에서 전체 흐름 익히기 | 아래 체크리스트 시뮬레이션 항목 완료 | |
| 1 Bringup | SBC에서 `ros2 launch tb3_team10 robot.launch.py`(내부에서 `turtlebot3_bringup` 실행) | Remote PC `ros2 topic list`에 `/scan`, `/odom`, `/imu`, `/battery_state`, `/tf`가 보인다 | |
| 2 텔레옵 | Remote PC에서 `ros2 run turtlebot3_teleop teleop_keyboard` | 바닥에서 전진, 후진, 회전이 되고 `s`나 스페이스로 바로 멈춘다 | |
| 3 SLAM | Remote PC에서 `ros2 launch tb3_team10 slam.launch.py` 후 텔레옵으로 지도 작성 | `ros2 run nav2_map_server map_saver_cli -f ~/map`으로 `map.pgm`, `map.yaml`이 생기고 RViz에서 벽이 겹치지 않는다. 쓸 지도는 레포 `src/tb3_team10/maps/`에 복사 | |
| 4 Nav2 | `ros2 launch tb3_team10 nav.launch.py map:=$HOME/map.yaml` (`map` 생략 시 팀 지도) | 2D Pose Estimate 후 스캔이 지도와 겹치고, Navigation2 Goal로 찍은 곳까지 부딪히지 않고 간다 | |
| 5 팀 과제 | 과제 코드를 `src/tb3_team10`에 추가 | `colcon build`가 경고 없이 끝나고, `/cmd_vel`을 쓰는 노드는 `TwistStamped`로 퍼블리시하며, 시뮬레이션에서 먼저 동작을 확인한 뒤 실물에서 돌린다. 과제 내용이 정해지면 이 칸을 구체화 | |

실물 단계에서는 `use_sim_time`을 붙이지 않는다. 시뮬레이션 launch에는 모두 `use_sim_time:=True`를 붙인다.

## B4. 진행 체크리스트

### Claude Code 환경
- [x] 프로젝트 전용 `~/workspace/CLAUDE.md` 작성 (Windows CLAUDE.md import)
- [x] scout/builder 에이전트 연결 (`~/workspace/.claude/agents/` → Windows 심볼릭 링크)
- [x] ADHD 모드 always-on (`~/.claude/.i-have-adhd-always`)
- [x] ponytail 설치, 프로젝트 범위로 활성화
- [x] Node.js 설치 → 두 SessionStart 훅 직접 실행해 동작 확인

### 시뮬레이션 (Gazebo)
- [x] Remote PC 패키지 설치
- [x] 환경변수 설정
- [x] `ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py` 실행 확인 (GUI segfault → `LIBGL_ALWAYS_SOFTWARE=1 GZ_IP=127.0.0.1`로 해결)
- [ ] `ros2 run turtlebot3_teleop teleop_keyboard`로 직접 조작 (미확인)
- [x] Cartographer SLAM → 지도 저장 `~/workspace/map.pgm/.yaml` (키보드 대신 `~/workspace/wander.py` 자동 주행으로 생성)
- [x] Nav2 자율주행: 초기 위치 지정 후 목표 `(-0.5, 0.5)` 도착 확인

지도 재현: Gazebo → `cartographer.launch.py use_sim_time:=True` → `python3 ~/workspace/wander.py 300` → `map_saver_cli -f ~/workspace/map`

### 조립 (A)
- [x] 부품 확인 (A1)
- [x] 1층부터 4층까지 조립 (A2)
- [x] 배선 점검, 특히 라즈베리파이 전원 핀 (A3)
- [x] 배터리 충전 확인 (A4)
- [x] microSD에 Ubuntu Server 24.04 설치, Wi-Fi·SSH 설정 (A5)
- [x] SBC 패키지 설치·빌드, udev 규칙, `LDS_MODEL` (A5)
- [x] OpenCR 펌웨어 업로드 (A6)
- [x] SW1 전진 30cm, SW2 180도 회전 (A7)

### 실물 개발 (B)
- [x] WSL mirrored 모드 전환
- [x] 1 Bringup: PC에서 `/scan`, `/odom` 확인 (2026-11-17, Cyclone 유니캐스트 피어 필요)
- [ ] 2 텔레옵
- [ ] 3 SLAM 지도 저장
- [ ] 4 Nav2 목표 도착
- [x] `src/tb3_team10` 패키지 생성, `colcon build` 통과, GitHub push
- [ ] `ros2 launch tb3_team10 sim.launch.py` 실행 확인
- [ ] 5 팀 과제 코드를 `tb3_team10`에 추가

## B5. 주의사항
- Jazzy부터 `/cmd_vel` 타입은 `TwistStamped`다. 직접 짠 퍼블리셔도 맞춰야 한다. `Twist`로 되돌리려면 `turtlebot3_bringup`과 `turtlebot3_navigation2`의 `enable_stamped_cmd_vel`을 false로 바꿔야 하는데, 우리는 기본값(TwistStamped)을 그대로 쓴다.
- Gazebo에서 재현 안 되는 것: 배터리 상태, OpenCR 버튼과 사운드, 실제 노이즈와 바퀴 슬립, PC와 SBC 사이 네트워크.
- Nav2 실행 중에는 텔레옵을 끈다(`/cmd_vel` 충돌).
- 실물 주행은 바닥에서만 한다. Nav2는 목표를 찍자마자 움직이니 주변을 먼저 비운다.

## 변경 메모

2026-10-13에 ROBOTIS e-Manual(Jazzy 탭)과 공식 Quick Start PDF(Rev.10)를 기준으로 고쳤다. 기존 내용과 다른 점은 다음과 같다.

- SBC에 `python3-argcomplete`, `libboost-system-dev`, `build-essential`을 추가했고, clone 후 `turtlebot3_cartographer`, `turtlebot3_navigation2`를 지우는 단계와 `--symlink-install`을 넣었다.
- SBC OS를 Ubuntu Server 24.04.2 LTS 64-bit로 구체화하고, 2GB 모델 스왑 안내와 udev 규칙 명령을 추가했다.
- Remote PC와 SBC 모두에 `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`를 추가했다. 기존 문서에는 없었다.
- e-Manual은 Remote PC의 TurtleBot3를 소스(`~/turtlebot3_ws`, jazzy 브랜치)로 빌드하고 Gazebo는 OSRF 저장소의 `gz-harmonic`으로 설치한다. 우리는 apt 설치로 시뮬레이션을 이미 확인했으므로 그대로 두고, 소스 빌드는 대안으로 적었다.
- e-Manual 지도 저장 경로는 `~/map`, 기존 시뮬레이션 기록은 `~/workspace/map`이다. 기록은 그대로 두었다.
- 2026-10-13: 팀 패키지 `tb3_team10`을 만들어 레포 `src/`에 올렸다. 시뮬과 실물 launch를 한 곳에서 실행하기 위해서다.
