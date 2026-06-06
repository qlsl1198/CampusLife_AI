from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def subject_particle(word: str) -> str:
    if not word:
        return "가"
    code = ord(word[-1])
    if 0xAC00 <= code <= 0xD7A3 and (code - 0xAC00) % 28:
        return "이"
    return "가"


def with_particle(word: str, consonant_form: str, vowel_form: str) -> str:
    if not word:
        return vowel_form
    code = ord(word[-1])
    if 0xAC00 <= code <= 0xD7A3 and (code - 0xAC00) % 28:
        return consonant_form
    return vowel_form


@dataclass
class Memory:
    subject: str
    fact: str
    day: int
    time: str
    source_round: int

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class Relation:
    target: str
    summary: str
    trust: int = 50
    talk_count: int = 0
    updated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class PlanSlot:
    day: int
    time: str
    location: str
    activity: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class Message:
    speaker: str
    text: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class ConversationRound:
    round_id: int
    day: int
    time: str
    location: str
    participants: list[str]
    messages: list[Message]
    extracted_facts: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "round_id": self.round_id,
            "day": self.day,
            "time": self.time,
            "location": self.location,
            "participants": self.participants,
            "messages": [message.to_dict() for message in self.messages],
            "extracted_facts": self.extracted_facts,
        }


@dataclass
class Agent:
    agent_id: str
    name: str
    age: int
    major: str
    personality: str
    goal: str
    memories: list[Memory] = field(default_factory=list)
    relations: dict[str, Relation] = field(default_factory=dict)
    plan: list[PlanSlot] = field(default_factory=list)

    def remember(self, memory: Memory) -> None:
        if all(item.fact != memory.fact or item.subject != memory.subject for item in self.memories):
            self.memories.append(memory)

    def facts_about(self, subject: str) -> list[str]:
        return [memory.fact for memory in self.memories if memory.subject == subject]

    def update_relation(self, target: "Agent", new_fact_count: int) -> None:
        relation = self.relations.get(target.agent_id)
        if relation is None:
            particle = with_particle(target.name, "과", "와")
            summary = f"{target.name}{particle} 처음 대화했고, {target.major} 분야에 관심이 있다는 인상을 받았다."
            relation = Relation(target=target.agent_id, summary=summary, trust=55, talk_count=1)
        else:
            relation.talk_count += 1
            relation.trust = min(100, relation.trust + 4 + new_fact_count)
            relation.summary = (
                f"{target.name}{with_particle(target.name, '과', '와')} {relation.talk_count}번 대화했다. "
                f"최근에는 {target.goal}에 대해 더 구체적으로 알게 되었다."
            )
            relation.updated_at = now_iso()
        self.relations[target.agent_id] = relation

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "age": self.age,
            "major": self.major,
            "personality": self.personality,
            "goal": self.goal,
            "memories": [memory.to_dict() for memory in self.memories],
            "relations": {key: value.to_dict() for key, value in self.relations.items()},
            "plan": [slot.to_dict() for slot in self.plan],
        }
