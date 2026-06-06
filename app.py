from __future__ import annotations

import argparse
import json
from pathlib import Path

from campuslife.models import Agent
from campuslife.simulation import SimulationEngine


ROOT = Path(__file__).resolve().parent


def load_agents(path: Path) -> list[Agent]:
    raw_agents = json.loads(path.read_text(encoding="utf-8"))
    return [Agent(**item) for item in raw_agents]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CampusLife AI multi-agent simulation")
    parser.add_argument("--days", type=int, default=2, help="시뮬레이션 일수")
    parser.add_argument("--turns", type=int, default=2, help="Agent당 발화 횟수")
    parser.add_argument("--agents", type=Path, default=ROOT / "data" / "agents.json", help="Agent JSON 경로")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs", help="산출물 저장 경로")
    parser.add_argument("--report-target", default="mina", help="리포트를 생성할 Agent ID")
    parser.add_argument("--print-report", action="store_true", help="생성된 Markdown 리포트를 터미널에 출력")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    agents = load_agents(args.agents)
    engine = SimulationEngine(
        agents=agents,
        days=args.days,
        turns_per_agent=args.turns,
        output_dir=args.output_dir,
    )
    result = engine.run(report_target=args.report_target)
    print(f"Simulation complete: {len(result['rounds'])} conversation rounds")
    print(f"Report saved: {result['report_path']}")
    if args.print_report:
        print()
        print(result["report"])


if __name__ == "__main__":
    main()
