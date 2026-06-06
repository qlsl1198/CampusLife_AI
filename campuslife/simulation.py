from __future__ import annotations

import json
from pathlib import Path

from .conversation import ConversationManager
from .models import Agent, ConversationRound
from .planner import DailyPlanner
from .report import MarkdownReporter


class SimulationEngine:
    def __init__(
        self,
        agents: list[Agent],
        days: int = 2,
        turns_per_agent: int = 2,
        output_dir: str | Path = "outputs",
    ) -> None:
        self.agents = agents
        self.days = days
        self.turns_per_agent = turns_per_agent
        self.output_dir = Path(output_dir)
        self.planner = DailyPlanner()
        self.conversations = ConversationManager()
        self.reporter = MarkdownReporter()
        self.rounds: list[ConversationRound] = []
        self.round_id = 0

    def run(self, report_target: str | None = None) -> dict:
        self._prepare_outputs()
        for day in range(1, self.days + 1):
            self._plan_day(day)
            self._run_day(day)
            self._save_json(self.output_dir / "states" / f"day{day}_state.json", self.state_dict())
        self._save_json(self.output_dir / "states" / "final_state.json", self.state_dict())
        target_id = report_target or self.agents[0].agent_id
        report = self.reporter.generate(target_id, self.agents, self.rounds)
        report_path = self.output_dir / "reports" / f"report_{target_id}_day{self.days}.md"
        report_path.write_text(report, encoding="utf-8")
        return {"rounds": self.rounds, "report_path": str(report_path), "report": report}

    def _plan_day(self, day: int) -> None:
        for index, agent in enumerate(self.agents):
            agent.plan = self.planner.create_plan(agent, day, index)

    def _run_day(self, day: int) -> None:
        times = self.planner.times
        for time in times:
            groups = self._groups_at(time)
            for location, members in groups.items():
                if len(members) < 2:
                    continue
                self.round_id += 1
                round_item = self.conversations.build_round(
                    self.round_id,
                    day,
                    time,
                    location,
                    sorted(members, key=lambda item: item.agent_id),
                    self.turns_per_agent,
                )
                self._update_relations(members, round_item)
                self.rounds.append(round_item)
                safe_location = location.replace("/", "_")
                log_path = self.output_dir / "logs" / f"day{day}_{time.replace(':', '')}_{safe_location}.json"
                self._save_json(log_path, round_item.to_dict())

    def _groups_at(self, time: str) -> dict[str, list[Agent]]:
        groups: dict[str, list[Agent]] = {}
        for agent in self.agents:
            slot = next(item for item in agent.plan if item.time == time)
            groups.setdefault(slot.location, []).append(agent)
        return groups

    def _update_relations(self, members: list[Agent], round_item: ConversationRound) -> None:
        for viewer in members:
            for target in members:
                if viewer.agent_id == target.agent_id:
                    continue
                new_fact_count = len(round_item.extracted_facts.get(target.agent_id, []))
                viewer.update_relation(target, new_fact_count)

    def state_dict(self) -> dict:
        return {
            "agents": [agent.to_dict() for agent in self.agents],
            "rounds": [round_item.to_dict() for round_item in self.rounds],
            "days": self.days,
        }

    def _prepare_outputs(self) -> None:
        for name in ["logs", "states", "reports"]:
            (self.output_dir / name).mkdir(parents=True, exist_ok=True)

    def _save_json(self, path: Path, data: dict) -> None:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
