# Spec 001 — `GET /progress`

## Why
A learner who has practised several rounds wants a one-glance answer to "how am I doing?" without reading `data/results.json` by hand. `/progress` gives the headline numbers over the API (and `/docs`), the same ones the `/report` skill summarises.

## What it returns
`GET /progress` takes no parameters and returns JSON:

```json
{"rounds_practised": 2, "average_total": 6.0}
```

| Field | Type | Meaning |
|---|---|---|
| `rounds_practised` | int | Number of saved results. |
| `average_total` | float \| null | Mean of each result's `total` (out of 20), rounded to 1 decimal. `null` when there are no results. |

## Acceptance criteria
1. With N ≥ 1 saved results, `rounds_practised` equals N and `average_total` equals the mean of `total`, rounded to one decimal place (e.g. totals 3 and 9 → `6.0`).
2. **Empty case:** with no saved results (missing file or `[]`), the response is `200` with `{"rounds_practised": 0, "average_total": null}`. It is never a 404 or 500, and no number is invented.
3. The endpoint is read-only: it never writes to `data/results.json`.
4. A malformed results file returns a structured JSON error, not a stack trace (per `CLAUDE.md`).
5. Tests cover the populated and empty cases using a temporary data directory, with no network.

## What it reads
- `data/results.json`, via `data.load_results()` only (all file access stays in `app/data.py`).
- Per entry it uses only `total`.

## Out of scope
- Per-category averages or the weakest category (that stays in `/report` for now).
- Filtering by round or date, history or trend over time.
- Maximum other than 20 (`max` is not read).
- Clearing or editing results.
- Authentication and multiple users.
