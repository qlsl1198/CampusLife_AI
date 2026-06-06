from __future__ import annotations

from .models import Agent, ConversationRound, subject_particle


class MarkdownReporter:
    def generate(self, target_id: str, agents: list[Agent], rounds: list[ConversationRound]) -> str:
        target = self._find_agent(target_id, agents)
        lines = [
            f"# {target.name} 관점의 CampusLife AI 리포트",
            "",
            "## 시뮬레이션 요약",
            f"- 참여 Agent 수: {len(agents)}",
            f"- 생성된 대화 라운드 수: {len(rounds)}",
            f"- {target.name}{subject_particle(target.name)} 기억한 사실 수: {len(target.memories)}",
            "",
            "## Agent별 기억과 관계",
        ]
        for agent in agents:
            if agent.agent_id == target.agent_id:
                continue
            lines.extend(self._agent_section(target, agent))
        lines.extend(["", "## 전체 대화 타임라인"])
        for round_item in rounds:
            names = ", ".join(round_item.participants)
            lines.append(f"- Day {round_item.day} {round_item.time} {round_item.location}: {names}")
        return "\n".join(lines) + "\n"

    def _agent_section(self, viewer: Agent, subject: Agent) -> list[str]:
        facts = viewer.facts_about(subject.agent_id)
        relation = viewer.relations.get(subject.agent_id)
        lines = ["", f"### {subject.name}", "", "#### 기억한 사실"]
        if facts:
            lines.extend(f"- {fact}" for fact in facts)
        else:
            lines.append("- 아직 기억한 사실이 없다.")
        lines.append("")
        lines.append("#### 관계 Reflection")
        if relation:
            lines.append(f"- 신뢰도: {relation.trust}/100")
            lines.append(f"- 대화 횟수: {relation.talk_count}")
            lines.append(f"- 요약: {relation.summary}")
        else:
            lines.append("- 아직 관계가 형성되지 않았다.")
        return lines

    def _find_agent(self, target_id: str, agents: list[Agent]) -> Agent:
        for agent in agents:
            if agent.agent_id == target_id:
                return agent
        raise ValueError(f"Unknown report target: {target_id}")
