# Tasks — Spec 001 `GET /progress`

Spec: [spec.md](spec.md). The endpoint already exists (`app/main.py`, `get_progress`) but has no tests, so the tasks lock in current behaviour first and then close the gap in criterion 4.

Each task is one small commit: change -> run -> `pytest -q` -> commit. Tasks 1–3 are independent of each other; task 4 builds on 1.

## 1. Test fixture: isolated results file
**Covers:** criterion 5 (setup).
**Do:** in `tests/test_progress.py`, add a fixture that points `app.data.DATA_DIR` at `tmp_path` (via `monkeypatch`) and a helper that writes a given list to `results.json` there.
**Done when:** a throwaway test using the fixture can write and read back a results file, and `data/results.json` is untouched.
**Review:** one new test file, no app changes.

## 2. Test: populated case
**Covers:** criteria 1 and 3.
**Do:** with results whose totals are 3 and 9, `GET /progress` returns `200` and `{"rounds_practised": 2, "average_total": 6.0}`. Add a rounding case (totals 3, 4, 4 -> `3.7`). Assert the file contents are unchanged after the call.
**Done when:** the tests pass against the existing endpoint with no app change.
**Review:** tests only.

## 3. Test: empty case
**Covers:** criterion 2.
**Do:** two tests: `results.json` missing, and `results.json` containing `[]`. Both return `200` and `{"rounds_practised": 0, "average_total": null}`.
**Done when:** both pass against the existing endpoint with no app change.
**Review:** tests only.

## 4. Structured error for a malformed results file
**Covers:** criterion 4.
**Depends on:** task 1.
**Do:**
- Write a failing test first: `results.json` containing invalid JSON makes `/progress` return a JSON error body (not a stack trace) with a non-200 status.
- Then handle it. Catch `json.JSONDecodeError` in `data.load_results()` and raise a small named error. In `main.py`, map it to an `HTTPException` with a plain message, e.g. "Results file is unreadable."
**Done when:** the new test passes, tasks 2–3 still pass, and the response body contains no traceback text.
**Review:** one change in `app/data.py`, one in `app/main.py`, one test. Check that `POST /score` is unaffected.

## 5. Final check
**Covers:** all criteria.
**Do:** run `pytest -q`, then `uvicorn app.main:app --reload` and call `/progress` from `/docs` against the real `data/results.json`.
**Done when:** the tests pass and the live response matches the numbers `/report` gives for the same file.
**Review:** no code change. Note the result in the commit or PR description.
