# CampusLife AI

CampusLife AI는 캠퍼스 안에서 여러 Agent가 하루 일정을 계획하고, 같은 장소에서 만났을 때 대화하며, 대화에서 얻은 사실을 기억으로 저장하고 관계 Reflection을 갱신하는 멀티 에이전트 생활 시뮬레이션 과제입니다.

외부 API나 LLM 서버가 없어도 실행되도록 deterministic mock 방식으로 만들었습니다. 
실행 결과는 JSON 로그와 Markdown 리포트로 저장됩니다.

## 주요 기능

- Agent 프로필 로딩
- Agent별 Daily Plan 생성
- 시간대와 장소 기준 자동 매칭
- 같은 장소 Agent 간 대화 라운드 생성
- 대화 기반 Fact 추출 및 Memory 저장
- Agent 간 Relation / Reflection 갱신
- 특정 Agent 관점의 최종 Markdown 리포트 생성
- pytest 기반 핵심 기능 테스트
- 제출용 zip 생성 스크립트 포함

## 실행 방법

Python 3.10 이상을 권장합니다. 별도 필수 패키지는 없습니다.

```bash
python app.py --print-report
```

옵션 예시:

```bash
python app.py --days 1 --turns 1 --report-target mina
```

## 산출물

실행 후 `outputs/` 폴더에 파일이 생성됩니다.

```text
outputs/
├── logs/       # 대화 라운드별 JSON
├── states/     # day별/final 상태 JSON
└── reports/    # Agent 관점 Markdown 리포트
```

## 테스트

```bash
python -m unittest discover -s tests
```

## 제출 zip 생성

```bash
python scripts/make_submission_zip.py
```

생성 결과:

```text
submission/CampusLife_AI_submission.zip
```

## 프로젝트 구조

```text
CampusLife_AI/
├── app.py
├── campuslife/
│   ├── models.py
│   ├── planner.py
│   ├── conversation.py
│   ├── simulation.py
│   └── report.py
├── data/
│   └── agents.json
├── docs/
│   └── project_plan.md
├── tests/
│   └── test_simulation.py
└── scripts/
    └── make_submission_zip.py
```
