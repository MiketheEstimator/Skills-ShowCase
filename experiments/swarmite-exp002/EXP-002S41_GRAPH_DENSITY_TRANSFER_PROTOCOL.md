# EXP-002S41 — Frozen Credal Gate under Graph-Density Shift

## Hypothesis
The S39 credal disagreement gate is not merely calibrated to the benchmark generator's edge probability 0.35. With S30 unchanged, the frozen gate should remain safe and useful when the true DAG distribution shifts toward substantially sparser or denser graphs.

## Frozen treatment
- S30 point posterior unchanged.
- Disagreement score: `mean_credal_width` unchanged.
- Threshold: `0.2692013432171404` unchanged.
- Promote S30 when score <= threshold; otherwise abstain to baseline.
- No specialist selection, averaging, or threshold retuning.

## Shifted graph generator
Retain five nodes, random topological order, coefficient signs, coefficient magnitudes Uniform(0.4,0.9), intervention budget, planner, and RNG isolation. Generate prospective DAGs from two unseen density regimes:
- sparse: edge probability 0.15,
- dense: edge probability 0.55.
As in benchmark v2, enforce at least two edges by deterministic fallback additions when required.

Use the committed S32 six mechanism/noise cells (`tanh/sin/asinh` × `gaussian/t7`) so graph density is the isolated shift dimension. Density alternates by six-seed blocks, producing balanced cell × density exposure.

Mechanics seeds: 72701–72704.
Screen seeds: 72711–72734 (24).
Confirmation seeds: 72801–72848 (48), exposed only after screen success.

## Screen gate
Advance only if mechanics hold and the frozen gate achieves coverage >= 0.60, promoted large-harm rate <= 0.05, hybrid mean edge delta vs baseline < 0, hybrid mean Brier delta <= +0.005, and >= 0.70 improvement retention whenever always-S30 is beneficial.

## Confirmation promotion
Require the same constraints plus bootstrap 95% upper bound for hybrid mean edge delta < 0.

## Interpretation
Success supports the S39 credal layer across both observation-model and graph-prior shift. Failure redirects to explicit topology-aware/world-class uncertainty rather than tuning the gate on these worlds.