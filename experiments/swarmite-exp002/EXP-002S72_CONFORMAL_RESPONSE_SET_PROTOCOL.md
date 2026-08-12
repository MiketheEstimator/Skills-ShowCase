# EXP-002S72 — Empirical Conformal Intervention-Response Set Diagnostic

## Status
Prospective protocol. Frozen before execution.

## Motivation
S69 established intervention-response predictive miscalibration. S70 and S71 then falsified global and richer conditional Gaussian moment recalibration. The next scientific question is whether a distribution-free empirical calibration layer can recover nominal response uncertainty without hidden-regime labels and without another parametric moment-model retune.

## Hypothesis
Split-conformal empirical response sets, grouped only by observable predictive dispersion and intervention setpoint, will reduce held-out nominal coverage error relative to the raw Gaussian posterior-predictive intervals while avoiding material regime-specific regression.

## Frozen controls
- Upstream benchmark/world generator and posterior simulator remain unchanged.
- Hidden regime labels are unavailable to calibration fitting and grouping; they are used only after inference for scoring.
- Raw posterior-predictive Gaussian intervals are the matched control.
- No S70/S71 coefficient, bin, shrinkage, or regression retuning is allowed.
- Calibration and held-out worlds are disjoint.

## Data partitions
- Mechanics: 2 fresh worlds per regime.
- Calibration: 64 fresh worlds per regime.
- Held-out: 64 fresh worlds per regime.
- Each world evaluates every intervention target at setpoints -2 and +2 with the same posterior-predictive draw budget used in S69-S71.

## Conformal representation
For every response cell, compute the posterior-predictive mean `mu`, predictive standard deviation `sd`, and realized response residual `r = y - mu`.

Calibration grouping is truth-free at deployment:
1. pool all calibration cells across hidden regimes;
2. stratify by intervention setpoint sign;
3. within each sign, split cells into five quantile bins of observable `log(sd)`;
4. in each cell group, store empirical residual quantiles for central 80% and 95% intervals.

The conformal interval is `mu + [q_lo, q_hi]`, using empirical asymmetric residual quantiles. If a group contains fewer than 100 calibration cells, back off to the setpoint-level pool. No Gaussian bias/scale model is fit.

## Metrics
For each hidden regime on held-out worlds:
- raw 80% and 95% coverage;
- conformal 80% and 95% coverage;
- mean interval width at 80% and 95%;
- nominal coverage error `|c80-.80| + |c95-.95|`.

Aggregate metrics:
- mean nominal coverage error across regimes;
- relative coverage-error improvement over raw control;
- width ratio versus raw Gaussian intervals.

## Frozen success criteria
`CONFORMAL_RESPONSE_SETS_SUPPORTED` only if all hold:
1. mean nominal coverage error improves by at least 20%;
2. neither regime's coverage error is worse than raw by more than 0.02;
3. conformal 80% coverage lies in [0.74, 0.86] for both regimes;
4. conformal 95% coverage lies in [0.91, 0.98] for both regimes;
5. mean conformal 95% width is no more than 1.75x the raw Gaussian 95% width.

Otherwise the scientific result is `CONFORMAL_RESPONSE_SETS_FALSIFIED`. Execution failures remain BLOCKED and do not count as falsification.

## Successor logic
- Supported: S73 retests branch-aware acquisition using the frozen conformal response sets without retuning the planner.
- Falsified: S73 abandons scalar/moment/coverage recalibration and tests set-valued acquisition utility directly from empirical intervention-response outcome families.
- Blocked: repair execution only; do not alter the scientific hypothesis.
