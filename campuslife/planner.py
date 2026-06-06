from __future__ import annotations

from .models import Agent, PlanSlot


DEFAULT_TIMES = ["09:00", "11:00", "13:00", "15:00", "17:00", "19:00"]
DEFAULT_LOCATIONS = ["기숙사", "강의실", "학생식당", "도서관", "동아리방", "카페"]


class DailyPlanner:
    def __init__(self, times: list[str] | None = None, locations: list[str] | None = None) -> None:
        self.times = times or DEFAULT_TIMES
        self.locations = locations or DEFAULT_LOCATIONS

    def create_plan(self, agent: Agent, day: int, agent_index: int) -> list[PlanSlot]:
        plan: list[PlanSlot] = []
        for index, time in enumerate(self.times):
            location = self.locations[(index + agent_index + day) % len(self.locations)]
            if time in {"13:00", "19:00"}:
                location = "학생식당"
            if time == "15:00" and (agent_index + day) % 2 == 0:
                location = "도서관"
            activity = self._activity_for(agent, location, time)
            plan.append(PlanSlot(day=day, time=time, location=location, activity=activity))
        return plan

    def _activity_for(self, agent: Agent, location: str, time: str) -> str:
        if location == "강의실":
            return f"{agent.major} 수업 듣기"
        if location == "도서관":
            return f"{agent.goal} 관련 자료 정리"
        if location == "동아리방":
            return "프로젝트 아이디어 회의"
        if location == "학생식당":
            return "식사하며 친구들과 근황 나누기"
        if location == "카페":
            return "과제 초안 작성"
        return "휴식 및 개인 정비"
