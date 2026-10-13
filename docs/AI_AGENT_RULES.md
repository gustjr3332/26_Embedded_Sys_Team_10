# AI 에이전트 협업 규칙

Claude Code 같은 AI 에이전트가 이 레포에서 작업할 때 따르는 규칙이다. 사람 팀원도 에이전트에게 일을 시키기 전에 한 번 읽어 두면 좋다.

## 환경 전제

- ROS 2 Jazzy, WSL2 Ubuntu 24.04, TurtleBot3 Burger.
- 작업 전에 `source scripts/env.sh`를 실행한다. 이 스크립트가 `TURTLEBOT3_MODEL=burger`, `LDS_MODEL=LDS-02`, `ROS_DOMAIN_ID`를 설정한다.
- Jazzy에서 `/cmd_vel`의 타입은 `geometry_msgs/TwistStamped`다. `Twist`로 쓰면 로봇이 움직이지 않는다.
- 시뮬레이션은 Gazebo Harmonic과 ros_gz를 쓰고, 모든 launch에 `use_sim_time:=True`를 준다.
- 공식 `turtlebot3*` 패키지는 apt로 설치한 것을 쓴다. 레포에 복사하지 않는다. 고쳐야 하면 `src/`에 우리 패키지를 만들어 launch와 params만 덮어쓴다.

## 브랜치와 PR

- `main`에는 직접 push하지 않는다. `feat/이름-내용` 브랜치를 만들고 PR을 올린다.
- 한 PR은 한 가지 일만 다룬다. 파일 이동, 포맷 변경, 기능 추가를 한 PR에 섞지 않는다.
- PR을 올리기 전에 `colcon build`를 실행해 통과를 확인한다. 시뮬이나 실물로 확인했으면 PR 본문에 어느 쪽인지 적는다.
- merge는 상대 팀원이 승인한 뒤에 한다. 에이전트가 스스로 승인하거나 merge하지 않는다.
- 커밋 메시지는 한국어로 쓰고, 에이전트가 만든 커밋 끝에는 `Co-Authored-By` 줄을 남긴다.

## 이 레포에 올리면 안 되는 것

레포가 public이라 한 번 push하면 기록에 남는다.

- 강의 PDF와 교재 파일
- Wi-Fi 이름과 비밀번호, SSH 키, 토큰, 라즈베리파이의 IP 주소
- `build/`, `install/`, `log/`, `*.Zone.Identifier`
- 개인 이메일. 커밋 이메일은 GitHub noreply 주소를 쓴다.

커밋 전에 `git status`와 `git diff --cached`로 위 항목이 섞이지 않았는지 확인한다.

## 에이전트가 먼저 물어봐야 하는 작업

아래 작업은 사용자가 그 자리에서 허락했을 때만 한다.

- `git push --force`, `git reset --hard`, 브랜치 삭제
- 파일이나 디렉터리 삭제, 다른 사람이 쓰던 파일 덮어쓰기
- `sudo`가 필요한 시스템 패키지 설치와 설정 변경
- 실물 로봇에 속도 명령을 보내는 작업. 로봇 주변이 비어 있는지 사람이 확인해야 한다.
- 레포 설정(보호 규칙, 협업자, 공개 범위) 변경

## 로봇 공유 규칙

- 개인 시뮬레이션은 팀원마다 `ROS_DOMAIN_ID`를 다르게 잡는다(A는 30, B는 31). 같은 Wi-Fi에서 domain이 겹치면 상대 토픽이 섞인다.
- 실물 로봇을 쓸 때만 로봇의 domain과 맞춘다. 로봇은 한 번에 한 사람이 쓰고, 쓰기 전에 팀 채팅에 알린다.
- 실물 연동에는 `.wslconfig`의 `networkingMode=mirrored`가 필요하다.

## 문서와 기록

- 설치나 실습 단계를 끝내면 `docs/SETUP.md`의 체크리스트를 갱신한다.
- 새로 만든 지도는 `maps/`에 넣고, 만든 방법을 PR 본문에 한 줄로 남긴다.
- 확인하지 못한 것은 확인했다고 쓰지 않는다. 테스트를 못 돌렸으면 못 돌렸다고 적는다.
