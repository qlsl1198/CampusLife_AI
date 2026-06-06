from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SUBMISSION_DIR = ROOT / "submission"
ZIP_PATH = SUBMISSION_DIR / "CampusLife_AI_submission.zip"
EXCLUDED_PARTS = {"__pycache__", ".git", ".venv", "submission", "outputs"}


def should_include(path: Path) -> bool:
    return not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)


def main() -> None:
    SUBMISSION_DIR.mkdir(exist_ok=True)
    with ZipFile(ZIP_PATH, "w", compression=ZIP_DEFLATED) as archive:
        for path in ROOT.rglob("*"):
            if path.is_file() and should_include(path):
                archive.write(path, path.relative_to(ROOT.parent))
    print(f"Created {ZIP_PATH}")


if __name__ == "__main__":
    main()
