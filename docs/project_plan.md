# CampusLife AI 기획서

## 1. 프로젝트 목표

이 프로젝트는 멀티 에이전트 시스템의 기본 구조를 캠퍼스 생활 시뮬레이션으로 구현한다. 각 Agent는 고유한 전공, 성격, 목표를 가지며 하루 일정을 생성한다. 같은 시간 같은 장소에 있는 Agent들은 대화하고, 대화에서 얻은 사실을 Memory로 저장한다. 반복 대화를 통해 Agent 간 관계 Reflection이 갱신된다.

## 2. 핵심 시나리오

1. `data/agents.json`에서 Agent 프로필을 불러온다.
2. 시뮬레이션 날짜별로 각 Agent의 계획을 생성한다.
3. 시간대별로 같은 장소에 모인 Agent를 찾는다.
4. 2명 이상이면 대화 라운드를 생성한다.
5. 대화에서 Agent별 사실을 추출해 상대방의 Memory에 저장한다.
6. 서로의 Relation을 갱신한다.
7. 최종 상태와 특정 Agent 관점의 Markdown 리포트를 저장한다.

## 3. 설계 포인트

- `models.py`: Agent, Memory, Relation, PlanSlot, ConversationRound 데이터 모델
- `planner.py`: deterministic daily plan 생성
- `conversation.py`: mock conversation 및 fact extraction
- `simulation.py`: 전체 시뮬레이션 루프와 산출물 저장
- `report.py`: 최종 Markdown 리포트 생성

## 4. 확장 가능성

- OpenAI/Ollama API를 연결해 대화와 계획 생성을 실제 LLM 응답으로 교체
- Streamlit 또는 Flask UI 추가
- 장소별 혼잡도, 친밀도 기반 만남 확률, Agent별 감정 상태 추가
- JSON 로그 기반 시각화 페이지 추가
