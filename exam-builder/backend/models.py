from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _uuid() -> str:
    return str(uuid.uuid4())


# --- Problem ---

class ProblemCreate(BaseModel):
    title: str
    description: str
    code: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None
    hint: Optional[str] = None
    solution: Optional[str] = None
    tags: list[str] = Field(default_factory=list)


class Problem(ProblemCreate):
    id: str = Field(default_factory=_uuid)
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


# --- Exam ---

class Section(BaseModel):
    title: str
    source_type: Literal["manual", "random"]
    problem_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    count: int = 0


class ExamCreate(BaseModel):
    title: str
    show_solutions: bool = False
    sections: list[Section] = Field(default_factory=list)


class Exam(ExamCreate):
    id: str = Field(default_factory=_uuid)
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


# --- Render result ---

class RenderedSection(BaseModel):
    title: str
    problems: list[Problem]


class RenderedExam(BaseModel):
    title: str
    show_solutions: bool
    sections: list[RenderedSection]
