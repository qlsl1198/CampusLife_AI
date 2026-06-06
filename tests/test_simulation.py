from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from campuslife.models import Agent
from campuslife.simulation import SimulationEngine


def sample_agents() -> list[Agent]:
    return [
        Agent("a", "Alice", 22, "AI", "calm", "finish the assignment"),
        Agent("b", "Bob", 23, "Data", "curious", "organize simulation logs"),
        Agent("c", "Celine", 21, "Design", "friendly", "write a readable report"),
    ]


class SimulationTest(unittest.TestCase):
    def test_run_creates_rounds_memories_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            engine = SimulationEngine(sample_agents(), days=1, turns_per_agent=1, output_dir=temp_dir)
            result = engine.run(report_target="a")

            self.assertGreater(len(result["rounds"]), 0)
            self.assertTrue(Path(result["report_path"]).exists())
            self.assertIn("Alice 관점", result["report"])
            self.assertGreater(len(engine.agents[0].relations), 0)

    def test_memory_does_not_store_self_fact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            engine = SimulationEngine(sample_agents(), days=1, turns_per_agent=1, output_dir=temp_dir)
            engine.run(report_target="a")

            for agent in engine.agents:
                self.assertEqual([], agent.facts_about(agent.agent_id))


if __name__ == "__main__":
    unittest.main()
