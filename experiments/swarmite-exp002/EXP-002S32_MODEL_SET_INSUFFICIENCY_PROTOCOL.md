# EXP-002S32 — Unseen-Regime Model-Set Insufficiency Diagnostic

## Status
Exploratory diagnostic frozen before any S32 world is executed.

## Motivation
S31 preserved significant aggregate benefit but failed transfer promotion because the frozen baseline+S23 model set did not improve `sin+Gaussian` and left `asinh+t7` unresolved. S32 isolates whether that boundary is driven primarily by mechanism mismatch, noise mismatch, or their interaction. No weighting-rule tuning is allowed.

## Frozen treatment
Use the exact S30/S31 terminal architecture without retuning:
- baseline planner only;
- baseline posterior `p0`;
- frozen S23 robust posterior `pr`;
- direct S29 ADEQ;
- `alpha = sigmoid(ADEQ/5.0)`;
- `pmix = (1-alpha)p0 + alpha pr`.

## Factorial regimes
Cross three structural mechanism transforms with two noise families:

Mechanisms:
1. `tanh`
2. `sin`
3. `asinh`

Noise:
1. `gaussian` — N(0,1)
2. `t7` — Student-t7 scaled to unit variance

Six cells total: `tanh_gaussian`, `tanh_t7`, `sin_gaussian`, `sin_t7`, `asinh_gaussian`, `asinh_t7`.

DAG generation, coefficients, planning, costs, budgets, and RNG discipline remain benchmark-v2.

## Worlds
Fresh seeds 71900-72019 (120 worlds, 20 per cell). Cell assignment is `seed % 6` and is used only by the simulator/evaluator, never by the terminal rule.

## Outcomes
For each cell report:
- mean mixed edge delta vs baseline and bootstrap 95% CI;
- mean mixed Brier delta;
- large harms > +0.50;
- mean ADEQ and mean alpha;
- always-robust edge delta for comparison.

Also report marginal means by mechanism and by noise.

## Diagnostic labels
- `SUPPORTED`: mean edge delta <0, bootstrap upper <0, mean Brier <= +0.010.
- `HARMFUL`: mean edge delta >0 with bootstrap lower >0, or mean Brier > +0.015.
- otherwise `UNRESOLVED`.

## Disposition logic
- If both `sin_gaussian` and `sin_t7` are HARMFUL/UNRESOLVED while tanh cells are SUPPORTED, diagnose **mechanism representation gap: sin**.
- If both t7 cells across non-sin mechanisms degrade relative to Gaussian while mechanism pattern is otherwise stable, diagnose **noise representation gap: t7**.
- If only specific combinations fail, diagnose **mechanism-noise interaction gap**.
- If all six are supported, S31 failure is sampling instability and the next experiment should replicate transfer on larger n rather than expand the model set.

## Redirect
S32 is diagnostic only. Any successor model-class expansion must be preregistered on entirely fresh worlds and must not train on S31/S32 worlds.
