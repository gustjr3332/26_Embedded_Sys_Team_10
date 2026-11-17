# tb3-team10 (TurtleBot3 Burger 팀 프로젝트)

## 작업 범위
- 터틀봇 프로젝트 작업은 전부 `~/tb3-team10`에서만 한다. `~/workspace`는 사용자가 따로 지시할 때만 건드린다.
- `~/workspace/src/team10`은 `~/tb3-team10/src/tb3_team10`을 가리키는 심볼릭 링크다. 사본을 만들지 않는다.
- 원격: github.com/gustjr3332/26_Embedded_Sys_Team_10. 작업 브랜치 `feat/slam-nav2`, 기준 브랜치 `main`.

## 환경
- WSL2 Ubuntu 24.04, ROS 2 Jazzy. 소스는 `src/tb3_team10`(launch: sim, slam, nav, robot), 환경 로드는 `source scripts/env.sh`.
- `TURTLEBOT3_MODEL=burger`, `ROS_DOMAIN_ID=25`, `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`. Remote PC와 SBC 값이 같아야 한다.
- `LDS_MODEL=LDS-02` (LD08, 115200bps, 패킷 헤더 `54 2C`). 드라이버는 `ld08_driver`. 2026-11-17 시리얼 원시 데이터와 라벨로 확인했다. LDS-03(`coin_d4_driver`)으로 잘못 적었던 기록은 고쳤다.
- Jazzy의 `/cmd_vel`은 `geometry_msgs/TwistStamped`다.
- 실물 연동 시 WSL은 `.wslconfig`의 `networkingMode=mirrored`가 필요하다(NAT에서는 DDS 디스커버리가 안 된다).
- SBC: Raspberry Pi 4, Ubuntu Server 24.04, `ros-jazzy-ros-base`. 미설치 단계는 `docs/SETUP.md` A5 순서대로 진행한다.

## 규칙
- 진행 상황의 정본은 `docs/SETUP.md`다. 단계를 끝내면 체크리스트를 갱신한다.
- 빌드는 `~/tb3-team10`에서 `colcon build --symlink-install --packages-select tb3_team10`. 그래야 `config/burger.yaml`(Nav2 튜닝 제출본)을 고친 뒤 재빌드 없이 Nav2 재실행만으로 반영된다. `build/ install/ log/`는 커밋하지 않는다.
- 커밋, 푸시, 브랜치 변경은 사용자가 요청할 때만 한다.
- 문서(README, SETUP.md)를 고칠 때는 `humanizer` 기준으로 쓴다.
- 자세한 절차는 `tb3-team10-workflow` 스킬을 따른다.
