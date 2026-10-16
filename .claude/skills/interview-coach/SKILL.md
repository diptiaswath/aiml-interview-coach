---
name: interview-coach
description: Run a mock AI/ML engineer interview round and score the answer against the rubric. Use when the user asks to "practise", "practice", "run a mock round", "mock interview", or "quiz me" on AI/ML interview questions.
---

# Interview coach

Run one mock interview round, one question at a time. Questions live in `data/questions.json` and the scoring rubric in `data/rubric.md`. Read both files at the start; don't rely on memory.

## Steps

1. **Ask which round.** List the distinct `round` values from `data/questions.json` (currently `ml-case`, `ml-system-design`, `genai-llm`, `behavioral`) and wait for the user to pick one. Don't pick for them.
2. **Present one question.** Choose one question from that round at random and show its `prompt`. Show only the question, with no hints, no rubric and no model answer. Then stop and wait for the answer.
3. **Take the answer.** Don't interrupt, and don't coach before scoring. If the answer is empty or clearly off-topic, say so and ask for another attempt instead of scoring it.
4. **Score it.** Score the answer against each of the four categories in `data/rubric.md`: Clarifying questions, Problem framing, Metrics & evaluation, Communication. Use the rubric's scale: 0 = absent, 1–2 = weak, 3 = solid, 4 = strong, 5 = exceptional. Give each category an integer 0–5 with a one-line reason that cites something the candidate actually said or left out. Add the four scores into a total out of 20.
5. **Give one improvement.** Give exactly one improvement, the change that would raise the score the most. Make it specific and actionable, not a list.
6. **Save the result.** After showing the scorecard, save it so `/report` can see it. Run this from the project root (`my-coach/`), with the JSON filled in. It goes through `app/data.py`, as `CLAUDE.md` requires:

   ```
   .venv/bin/python -c "import json, sys; from app import data; data.save_result(json.load(sys.stdin))" <<'EOF'
   {"round": "<round>", "question_id": "<question id>", "total": <int>, "max": 20,
    "categories": [{"name": "Clarifying questions", "score": <int>, "max": 5, "feedback": "<why>"},
                   {"name": "Problem framing", "score": <int>, "max": 5, "feedback": "<why>"},
                   {"name": "Metrics & evaluation", "score": <int>, "max": 5, "feedback": "<why>"},
                   {"name": "Communication", "score": <int>, "max": 5, "feedback": "<why>"}],
    "summary": "<the one improvement>"}
   EOF
   ```

   Use the same scores and wording you showed the user. Don't save a round that wasn't scored (empty or off-topic answers). If the command fails, tell the user the save failed and show the error. Don't edit `data/results.json` by hand.
7. **Offer another round.** Ask whether they want another question, a different round, or to stop.

## Output format

```
Question (<question id>, <round>): <prompt>

| Category | Score | Why |
|---|---|---|
| Clarifying questions | x/5 | ... |
| Problem framing | x/5 | ... |
| Metrics & evaluation | x/5 | ... |
| Communication | x/5 | ... |

Total: xx/20

One improvement: <single concrete change>
```

## Rules

- Score only what the candidate said. Don't give credit for things they probably knew.
- Be honest and calibrated. A 3 is solid; reserve 5 for exceptional answers.
- Never reveal the rubric criteria before the answer is given.
- Scoring is done by you, in conversation. Don't call the API or `POST /score`. The only write is the `data.save_result` call in step 6.
