"""FastAPI app for the AI/ML Interview Prep Assistant.

Run it:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs  -- the interactive API page is our "UI".
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException

from . import data, scoring
from .models import Question, ScoreRequest, ScoreResponse

app = FastAPI(title="AI/ML Interview Prep Assistant")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check."""
    return {"status": "ok"}


@app.get("/rounds")
def get_rounds() -> list[str]:
    """List the available interview round types."""
    return data.load_rounds()


@app.get("/questions")
def get_questions(round: str) -> list[Question]:
    """Return the questions for one round, e.g. /questions?round=ml-case."""
    questions = data.load_questions(round=round)
    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions for round '{round}'")
    return questions


@app.get("/progress")
def get_progress() -> dict:
    """Count of scored answers and their average total."""
    try:
        results = data.load_results()
    except data.ResultsUnreadableError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    if not results:
        return {"rounds_practised": 0, "average_total": None}
    average = sum(r["total"] for r in results) / len(results)
    return {"rounds_practised": len(results), "average_total": round(average, 1)}


@app.post("/score")
def post_score(request: ScoreRequest) -> ScoreResponse:
    """Score a candidate's answer and save the result."""
    scorecard = scoring.score_answer(request.answer)
    data.save_result(
        {"round": request.round, "question_id": request.question_id, **scorecard.model_dump()}
    )
    return scorecard
