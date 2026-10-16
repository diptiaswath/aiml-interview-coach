# CLAUDE.md — AI/ML Interview Prep Assistant

## What we're building
A small FastAPI app that runs mock AI/ML engineer interviews and
scores the answers against a rubric. Favour **clarity over cleverness** — every
line should be explainable in an interview.

## Stack
- Python 3.11+, **FastAPI** (served by uvicorn), **Pydantic v2**
- Data: plain **JSON files** in `data/` — no database
- Scoring: an offline **mock** scorer, or the **OpenAI API** when a key is set
  (the model id lives in one constant, `app/config.MODEL_ID`)
- Tests: **pytest** — never call the network in a test

## Project layout
- `app/` — the FastAPI app (endpoints, scoring, schemas, data access, config)
- `data/` — question bank, rubric, and saved results (JSON/markdown)
- `resources/` — interview guides
- `tests/` — pytest tests

## Conventions
- Type-hint everything; keep functions small and named for what they do.
- All file reads/writes go through `app/data.py`.
- Return structured JSON errors; never leak a stack trace to the client.

## Guardrails for you, the agent
- Show me the plan before large changes, and the diff before applying.
- Build in small steps: one feature -> run it -> test it -> commit.
- Never commit .env or any secret.

## How to run
```
python -m venv .venv
source .venv/bin/activate         # macOS/Linux  (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
uvicorn app.main:app --reload     # open http://127.0.0.1:8000/docs
pytest -q
```
