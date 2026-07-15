from __future__ import annotations

import random
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import storage
from models import (
    Exam,
    ExamCreate,
    Problem,
    ProblemCreate,
    RenderedExam,
    RenderedSection,
    _now,
)

app = FastAPI(title="Exam Builder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Problems ----

@app.get("/api/problems", response_model=list[Problem])
def list_problems(tags: Optional[str] = Query(None)):
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else None
    return storage.list_problems(tag_list)


@app.post("/api/problems", response_model=Problem, status_code=201)
def create_problem(body: ProblemCreate):
    problem = Problem(**body.model_dump())
    return storage.save_problem(problem)


@app.get("/api/problems/{problem_id}", response_model=Problem)
def get_problem(problem_id: str):
    p = storage.get_problem(problem_id)
    if not p:
        raise HTTPException(404, "Problem not found")
    return p


@app.put("/api/problems/{problem_id}", response_model=Problem)
def update_problem(problem_id: str, body: ProblemCreate):
    existing = storage.get_problem(problem_id)
    if not existing:
        raise HTTPException(404, "Problem not found")
    updated = Problem(
        id=existing.id,
        created_at=existing.created_at,
        updated_at=_now(),
        **body.model_dump(),
    )
    return storage.save_problem(updated)


@app.delete("/api/problems/{problem_id}", status_code=204)
def delete_problem(problem_id: str):
    if not storage.delete_problem(problem_id):
        raise HTTPException(404, "Problem not found")


@app.get("/api/tags", response_model=list[str])
def list_tags():
    return storage.all_tags()


# ---- Exams ----

@app.get("/api/exams", response_model=list[Exam])
def list_exams():
    return storage.list_exams()


@app.post("/api/exams", response_model=Exam, status_code=201)
def create_exam(body: ExamCreate):
    exam = Exam(**body.model_dump())
    return storage.save_exam(exam)


@app.get("/api/exams/{exam_id}", response_model=Exam)
def get_exam(exam_id: str):
    e = storage.get_exam(exam_id)
    if not e:
        raise HTTPException(404, "Exam not found")
    return e


@app.put("/api/exams/{exam_id}", response_model=Exam)
def update_exam(exam_id: str, body: ExamCreate):
    existing = storage.get_exam(exam_id)
    if not existing:
        raise HTTPException(404, "Exam not found")
    updated = Exam(
        id=existing.id,
        created_at=existing.created_at,
        updated_at=_now(),
        **body.model_dump(),
    )
    return storage.save_exam(updated)


@app.delete("/api/exams/{exam_id}", status_code=204)
def delete_exam(exam_id: str):
    if not storage.delete_exam(exam_id):
        raise HTTPException(404, "Exam not found")


@app.get("/api/exams/{exam_id}/render", response_model=RenderedExam)
def render_exam(exam_id: str):
    exam = storage.get_exam(exam_id)
    if not exam:
        raise HTTPException(404, "Exam not found")

    rendered_sections: list[RenderedSection] = []

    for section in exam.sections:
        if section.source_type == "manual":
            problems = []
            for pid in section.problem_ids:
                p = storage.get_problem(pid)
                if p:
                    problems.append(p)
            rendered_sections.append(
                RenderedSection(title=section.title, problems=problems)
            )

        elif section.source_type == "random":
            pool = storage.list_problems(section.tags if section.tags else None)
            count = min(section.count, len(pool))
            selected = random.sample(pool, count) if count > 0 else []
            rendered_sections.append(
                RenderedSection(title=section.title, problems=selected)
            )

    return RenderedExam(
        title=exam.title,
        show_solutions=exam.show_solutions,
        sections=rendered_sections,
    )
