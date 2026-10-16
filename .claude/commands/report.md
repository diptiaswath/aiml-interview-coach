---
description: Summarise practice progress from data/results.json
allowed-tools: Read
---

Read `data/results.json` and summarise my interview practice.

Each entry in the file looks like this:

```
{"round": ..., "question_id": ..., "total": <int out of 20>, "max": 20,
 "categories": [{"name": ..., "score": <0-5>, "feedback": ...}, ...], "summary": ...}
```

If the file is missing, empty, or contains no entries, reply only with "No results yet. Run a mock round first (try /interview-coach)." and stop. Don't invent numbers.

Otherwise report:

1. **Rounds practised**: the number of entries.
2. **Average total**: the mean of `total` across entries, to one decimal place, shown as `x.x / 20`.
3. **Weakest category**: average each category's `score` by `name` across all entries and name the lowest one with its average out of 5. If categories tie, name all of them.
4. **Focus next**: one concrete thing to work on, based on the weakest category and the `feedback` text for it in the entries. Name one action, not a list.

Keep it short. Use the numbers from the file only, and don't modify it.
