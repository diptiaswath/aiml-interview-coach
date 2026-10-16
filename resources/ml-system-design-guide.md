# Guide: The ML / GenAI System-Design Round

Design an end-to-end ML or LLM system and defend its quality, cost, and latency.

**A reliable pattern to reach for**
- **Ground it** — retrieval over real data (RAG); cite sources.
- **Constrain it** — schemas/tools instead of free text; validate outputs.
- **Evaluate it** — an eval set + LLM-as-judge as a deploy gate, not vibes.
- **Guardrail it** — PII handling, cost controls (caching, model routing),
  human-in-the-loop where the cost of error is high.
- **Operate it** — monitoring, drift detection, a retrain/refresh plan.

**Defend:** how you measure quality, what happens when the model is unsure, and
how cost and latency scale with usage.
