# aiml-interview-coach

A small FastAPI app for practising AI/ML engineer interviews. Pick a round, answer a question, and get a score against a four-category rubric (clarifying questions, problem framing, metrics & evaluation, communication), each out of 5.

## What it does

| Endpoint | Purpose |
|---|---|
| `GET /health` | Liveness check |
| `GET /rounds` | List round types (`ml-case`, `ml-system-design`, `genai-llm`, `behavioral`) |
| `GET /questions?round=...` | Questions for one round |
| `POST /score` | Score an answer and save the result to `data/results.json` |
| `GET /progress` | Rounds practised and average total (out of 20) |

Data lives in plain JSON files under `data/`, and interview guides are markdown in `resources/`. Scoring uses an offline mock scorer; the OpenAI path (`OPENAI_API_KEY`) is still a stub that falls back to the mock.

## How it was built

Built with Claude Code in small steps (one feature, run it, test it, commit), following the rules in `CLAUDE.md`.

- **Spec-driven:** `GET /progress` went from a plan (`plans/`) to a spec and five small tasks (`specs/001-progress-endpoint/`), then was implemented and checked against each acceptance criterion.
- **Tests:** pytest, with no network calls. File-based tests run against a temp data directory.
- **Hooks:** `.claude/hooks` blocks reading `.env` files and runs ruff and mypy after each edit.
- **MCP:** `mcp/server.py` exposes the guides as `list_guides` and `get_guide` tools (see `.mcp.json`).
- **Skills:** `.claude/skills/interview-coach` runs a mock round and saves the scorecard, and `/report` summarises progress.

## Run it

```
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload     # open http://127.0.0.1:8000/docs
pytest -q
```
