from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from models import Problem, Exam

DATA_DIR = Path(__file__).parent / "data"
PROBLEMS_DIR = DATA_DIR / "problems"
EXAMS_DIR = DATA_DIR / "exams"


def _ensure_dirs() -> None:
    PROBLEMS_DIR.mkdir(parents=True, exist_ok=True)
    EXAMS_DIR.mkdir(parents=True, exist_ok=True)


_ensure_dirs()


# --- generic helpers ---

def _save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# --- Problems ---

def list_problems(tags: Optional[list[str]] = None) -> list[Problem]:
    problems = []
    for f in sorted(PROBLEMS_DIR.glob("*.json")):
        p = Problem(**_load_json(f))
        if tags:
            if not all(t in p.tags for t in tags):
                continue
        problems.append(p)
    return problems


def get_problem(problem_id: str) -> Optional[Problem]:
    path = PROBLEMS_DIR / f"{problem_id}.json"
    if not path.exists():
        return None
    return Problem(**_load_json(path))


def save_problem(problem: Problem) -> Problem:
    path = PROBLEMS_DIR / f"{problem.id}.json"
    _save_json(path, problem.model_dump())
    return problem


def delete_problem(problem_id: str) -> bool:
    path = PROBLEMS_DIR / f"{problem_id}.json"
    if not path.exists():
        return False
    path.unlink()
    return True


def all_tags() -> list[str]:
    tag_set: set[str] = set()
    for f in PROBLEMS_DIR.glob("*.json"):
        data = _load_json(f)
        for t in data.get("tags", []):
            tag_set.add(t)
    return sorted(tag_set)


# --- Exams ---

def list_exams() -> list[Exam]:
    exams = []
    for f in sorted(EXAMS_DIR.glob("*.json")):
        exams.append(Exam(**_load_json(f)))
    return exams


def get_exam(exam_id: str) -> Optional[Exam]:
    path = EXAMS_DIR / f"{exam_id}.json"
    if not path.exists():
        return None
    return Exam(**_load_json(path))


def save_exam(exam: Exam) -> Exam:
    path = EXAMS_DIR / f"{exam.id}.json"
    _save_json(path, exam.model_dump())
    return exam


def delete_exam(exam_id: str) -> bool:
    path = EXAMS_DIR / f"{exam_id}.json"
    if not path.exists():
        return False
    path.unlink()
    return True
