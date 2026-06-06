from __future__ import annotations

from .models import Agent, ConversationRound, Memory, Message


class ConversationManager:
    def build_round(
        self,
        round_id: int,
        day: int,
        time: str,
        location: str,
        participants: list[Agent],
        turns_per_agent: int,
    ) -> ConversationRound:
        messages: list[Message] = []
        for turn in range(turns_per_agent):
            for speaker in participants:
                others = [agent for agent in participants if agent.agent_id != speaker.agent_id]
                target = others[turn % len(others)]
                messages.append(Message(speaker=speaker.name, text=self._line(speaker, target, location, turn)))
        facts = self.extract_facts(participants, round_id, day, time)
        return ConversationRound(
            round_id=round_id,
            day=day,
            time=time,
            location=location,
            participants=[agent.agent_id for agent in participants],
            messages=messages,
            extracted_facts=facts,
        )

    def extract_facts(
        self,
        participants: list[Agent],
        round_id: int,
        day: int,
        time: str,
    ) -> dict[str, list[str]]:
        facts: dict[str, list[str]] = {}
        for agent in participants:
            facts[agent.agent_id] = [
                f"{agent.name}의 전공은 {agent.major}이다.",
                f"{agent.name}의 현재 목표는 '{agent.goal}'이다.",
            ]
            for listener in participants:
                if listener.agent_id == agent.agent_id:
                    continue
                for fact in facts[agent.agent_id]:
                    listener.remember(Memory(agent.agent_id, fact, day, time, round_id))
        return facts

    def _line(self, speaker: Agent, target: Agent, location: str, turn: int) -> str:
        if turn == 0:
            return (
                f"{target.name}님, 저는 {speaker.major}을 공부하는 {speaker.name}입니다. "
                f"요즘은 {speaker.goal}에 집중하고 있어요."
            )
        return (
            f"{location}에서 이야기해보니 {target.name}님의 관점이 도움이 되네요. "
            f"제 성격은 {speaker.personality} 쪽이라 계획을 조금 더 세워보고 싶어요."
        )
