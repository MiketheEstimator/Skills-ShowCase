# EXP-002S36 — Global Stacking Transfer-Failure Diagnostic

## Status
PENDING until execution marks RUNNING.

## Rationale
S35 learned a frozen seven-class convex science-posterior stack from separated training worlds, but even its training minimax objective remained worse than frozen S30 and prospective validation was unresolved/slightly harmful. S34 simultaneously showed that useful represented classes exist per world. S36 tests whether the failure is (a) approximate-search error, (b) training-distribution instability, (c) regime heterogeneity that defeats any single global stack, or (d) remaining model-set insufficiency.

## Frozen diagnostic
Reuse only the already exposed S35 training worlds (72201–72248) and validation worlds (72261–72296). Reconstruct class terminal edge errors and S30 edge errors exactly.

Use exact linear programming over the seven-class simplex to solve, separately on training and validation:
- global minimax weights minimizing the maximum factorial-cell mean edge-error delta versus S30;
- report global mean delta under those weights;
- cross-evaluate training-optimal weights on validation and validation-optimal weights on training.

For each factorial cell, also report the best represented class by mean edge delta versus S30. Separately report per-world oracle represented-class coverage (fraction of worlds where at least one class beats S30).

## Diagnostic dispositions
1. `APPROXIMATE_SEARCH_FAILURE` if exact training minimax worst-cell delta < 0 but S35 random-search training worst-cell delta was >= 0.
2. `TRAIN_DISTRIBUTION_INSTABILITY` if exact training minimax worst-cell delta < 0, validation minimax worst-cell delta < 0, but training-optimal weights have validation worst-cell delta > +0.05.
3. `REGIME_HETEROGENEITY_FIXED_STACK_INSUFFICIENT` if global minimax worst-cell delta >= 0 on both training and validation, every factorial cell has at least one represented class with mean delta < 0 on its own data, and per-world oracle coverage >= 0.80 on both splits.
4. `MODEL_SET_INSUFFICIENCY` if per-world oracle coverage < 0.80 on either split or any cell lacks a represented class with negative mean delta.
5. `MIXED_FAILURE` otherwise.

## Scientific meaning
This experiment is diagnostic only. Ground truth is used retrospectively to identify the failure geometry. No deployment selector is trained and no new treatment is promoted.

## Invariants
- No new worlds.
- Exact LP replaces approximate candidate search only for diagnosis.
- No tuning of S35 weights or S30.
- Preserve planning traces and negative results.
- Google Drive remains read-only.
