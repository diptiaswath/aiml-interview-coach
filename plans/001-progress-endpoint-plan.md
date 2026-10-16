# Plan 001: `GET /progress` endpoint

## Goal
Add `GET /progress`. It reads `data/results.json` and returns:
- how many rounds have been practised
- the average total score

**Starting point:** `results.json` is `[]`. Nothing writes to it yet, because `POST /score`
is still a stub and `data.save_result()` accepts any `dict`.

## 1. Changes by file

| File | Change |
|---|---|
| `app/models.py` | Add `ProgressResponse(rounds_practised: int, average_total: float \| None)`. The average is `None` when there are no results. |
| `app/data.py` | Add `load_results() -> list[dict]`. It reads `DATA_DIR / "results.json"` and returns `[]` if the file is missing. All disk access stays in this file, per CLAUDE.md. |
| `app/main.py` | Add `@app.get("/progress") -> ProgressResponse` (details below). |
| `tests/test_progress.py` *(new)* | One test for the endpoint (details below). |

**Endpoint logic (`app/main.py`):**
1. Call `data.load_results()`.
2. **Empty guard:** if the list is empty, return `rounds_practised=0, average_total=None` straight away, so we never divide by zero.
3. Otherwise, count the records and average their `total` values, rounded to 1 decimal place.

**The test (`tests/test_progress.py`):**
- Monkeypatch `app.data.DATA_DIR` to a `tmp_path` holding an empty `results.json` (`[]`).
- Call `GET /progress`.
- Assert status `200` and body `{"rounds_practised": 0, "average_total": None}`.
- This covers the divide-by-zero guard, the riskiest path.

## 2. Order of work
1. Add the model.
2. Add `load_results()`.
3. Add the endpoint, including the empty guard.
4. Write the one test.
5. Run `pytest -q`, then check `curl /progress` against uvicorn.
6. Commit. This is one small step, per the guardrails.

## 3. What could break
- **Divide by zero** on an empty `results.json`. This is the current real state.
- **Tests touching the real `data/results.json`.** Patch `app.data.DATA_DIR`, not
  `app.config.DATA_DIR`. `data.py` does `from .config import DATA_DIR`, so patching `config` has no effect.
- **"Rounds practised" is ambiguous.** It could mean scored attempts or distinct round types.
  This plan counts attempts (`len(results)`).
- **Missing or corrupt file.** Handle a missing file. Let a corrupt file fail loudly (500).
- **Skewed averages.** Totals saved before the `compute_total()` fix will be too low.

## 4. Riskiest assumption
**Every record in `results.json` has a numeric `total` key.**

Nothing defines that shape yet. `/score` doesn't save anything, and `save_result()` takes any
`dict`. If the Module 3 `/score` work saves a different shape, `/progress` breaks.

**Mitigation:** when wiring `/score`, save the `ScoreResponse` fields plus `round` and
`question_id`, so `total` is guaranteed.

## Verification
- `pytest -q`: the existing tests and the new progress test pass.
- `uvicorn app.main:app --reload`, then `curl http://127.0.0.1:8000/progress`
  should return `{"rounds_practised": 0, "average_total": null}`.
