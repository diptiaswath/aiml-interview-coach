"""Load the question bank and rubric, and read/write results.

All disk access lives here, so the rest of the app never touches JSON files
directly. If storage ever moved to a database, this is the only file to change.
"""
from __future__ import annotations

import json

from .config import DATA_DIR, RESOURCES_DIR
from .models import Question


class ResultsUnreadableError(Exception):
    """Raised when data/results.json exists but is not valid JSON."""


def load_rounds() -> list[str]:
    """Return the available round types, derived from the question bank."""
    questions = load_questions()
    # dict.fromkeys keeps first-seen order and drops duplicates.
    return list(dict.fromkeys(q.round for q in questions))


def load_questions(round: str | None = None) -> list[Question]:
    """Load all questions, optionally filtered to a single round."""
    raw = json.loads((DATA_DIR / "questions.json").read_text(encoding="utf-8"))
    questions = [Question(**item) for item in raw]
    if round is not None:
        questions = [q for q in questions if q.round == round]
    return questions


def load_rubric() -> str:
    """Return the scoring rubric as markdown text."""
    return (DATA_DIR / "rubric.md").read_text(encoding="utf-8")


def load_results() -> list[dict]:
    """Return all saved results (empty list if none).

    Raises ResultsUnreadableError if the file exists but is not valid JSON.
    """
    path = DATA_DIR / "results.json"
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ResultsUnreadableError("Results file is unreadable.") from error


def save_result(record: dict) -> None:
    """Append one scored result to data/results.json."""
    path = DATA_DIR / "results.json"
    results = json.loads(path.read_text(encoding="utf-8"))
    results.append(record)
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")


def list_guide_names() -> list[str]:
    """Return the guide names (file stems of the .md files in resources/), sorted."""
    return sorted(path.stem for path in RESOURCES_DIR.glob("*.md"))


def load_guide(name: str) -> str:
    """Return one guide's markdown. Raises FileNotFoundError if it doesn't exist."""
    # Match against the known names so `name` can never point outside resources/.
    if name not in list_guide_names():
        raise FileNotFoundError(f"No guide named '{name}'.")
    return (RESOURCES_DIR / f"{name}.md").read_text(encoding="utf-8")
