# Guide: The ML Case / Problem-Framing Round

The most common AI/ML round. You're handed a vague business goal and asked how
you'd turn it into a working ML solution.

**What great looks like**
1. **Clarify first** — the business goal, the data you have (volume, labels,
   quality), constraints (latency, cost, privacy), and how success is measured.
2. **Frame the ML task** — classification, regression, ranking, generation? Define
   the target, the inputs, and what a prediction is used *for*.
3. **Start with a baseline** — a simple rule or model first, so you know what
   "better" means before reaching for something complex.
4. **Pick the right metric and validation** — precision/recall/F1/AUC vs accuracy
   (watch class imbalance), a leak-free split, and an online success measure.
5. **Name the failure modes** — data leakage, drift, bias, and how you'd monitor.

**Anti-patterns:** jumping to a model before framing the problem; reporting
accuracy on imbalanced data; no baseline; no definition of success.
