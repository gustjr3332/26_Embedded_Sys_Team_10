# 26 임베디드시스템 10조 — TurtleBot3 Burger

ROS 2 Jazzy · WSL2 Ubuntu 24.04 · TurtleBot3 Burger (Gazebo Harmonic)

## 시작
```bash
git clone https://github.com/gustjr3332/26_Embedded_Sys_Team_10.git ~/tb3 && cd ~/tb3
source scripts/env.sh
colcon build
```
- 진행 상황·설치 체크리스트: [docs/SETUP.md](docs/SETUP.md)
- 지도: `maps/`
- AI 에이전트 규칙: [docs/AI_AGENT_RULES.md](docs/AI_AGENT_RULES.md)

## 협업 규칙
- `main` 직접 push 금지. `feat/이름-내용` 브랜치 → PR → 상대 승인 후 merge.
- 강의 PDF·비밀번호·Wi-Fi 정보는 올리지 않는다 (public 레포).
