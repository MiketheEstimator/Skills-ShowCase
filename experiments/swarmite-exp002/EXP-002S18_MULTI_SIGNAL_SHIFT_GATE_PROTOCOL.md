# EXP-002S18 — Multi-Signal Model-Shift Abstention Gate

Status: RUNNING after protocol freeze.

## Hypothesis
S17 shows that total planning-vs-science edge-marginal disagreement alone is not sufficient under compound shift. A small preregistered gate combining independent observable disagreement signals can preserve the structural advantage of the frozen science posterior while rejecting the overconfident/miscalibrated cases that defeat the one-dimensional D gate.

## Frozen architecture
Use the exact S17 compound-shift environment and runner semantics: benchmark-v2 DAG/coefficient generation, `tanh(parent)` mechanisms, standardized Student-t(df=3) innovations with five innovations drawn as one vector before topological traversal, Gaussian benchmark-v2 planning posterior/controller, and frozen S5 nonlocal terminal science posterior. No terminal science quantity influences planning.

For each world compute only observable planning-vs-science quantities:
- `D_sum = sum(abs(edge_marginals(science)-edge_marginals(planning)))`.
- `D_max = max(abs(edge_marginals(science)-edge_marginals(planning)))`.
- `R_entropy = entropy(science) / max(entropy(planning), 1e-12)`.

A candidate gate promotes only when all three conditions hold: `D_sum <= a`, `D_max <= b`, and `R_entropy >= c`.

## Training
Fresh seeds 69301-69324. Candidate grid:
- a in {0.75, 1.00, 1.25, 1.50, 2.00}
- b in {0.25, 0.35, 0.45, 0.55, 0.70}
- c in {0.35, 0.50, 0.65, 0.80}

Evaluate truth only after each world terminates. A candidate qualifies if training coverage >=0.50, promoted mean edge delta <= -0.10, promoted mean Brier delta <= +0.005, and <=2 promoted worlds have edge harm >0.50. Select the highest-coverage qualifying gate. Break exact coverage ties by lower promoted mean Brier delta, then lower promoted mean edge delta, then lexicographically stricter `(a,b,-c)` to avoid post-hoc complexity.

Persist the complete training grid and selected gate before opening validation worlds.

## Validation
Fresh seeds 69401-69424. Pass only if coverage >=0.50, promoted mean edge delta <= -0.10, promoted mean Brier delta <= +0.005, <=2 promoted large harms, and exact planning-trace identity.

## Held-out confirmation
Only if validation passes: seeds 69501-69548. Promotion requires coverage >=0.50, promoted mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, promoted mean Brier delta <= +0.005, <=4 promoted large harms, and exact planning-trace identity.

## Interpretation boundary
Success supports a generalized abstention mechanism, not a claim that abstained worlds are solved. If the training grid cannot qualify or validation fails, redirect to posterior predictive residual diagnostics or explicit model-class uncertainty rather than retuning these signals on exposed worlds.