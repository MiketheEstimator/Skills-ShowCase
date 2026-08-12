# EXP-002S22 — Robust Model-Class Posterior Aggregation

Status: RUNNING after protocol freeze.

## Rationale
S21 established an evidence-dominance failure: marginal evidence almost always selected the nonlocal-tanh class even though it was never the truth-evaluated best represented class on the fresh diagnostic worlds. The represented class set therefore contains useful structural models, but raw marginal-evidence weighting is grossly overconfident under compound shift.

## Hypothesis
Tempering model-class marginal evidence before posterior pooling can preserve full coverage, retain the benefits of useful represented classes, and prevent a single misspecified class from dominating terminal inference.

## Frozen architecture
Use the exact S17 compound nonlinear + heavy-tail environment and exact unchanged baseline planning posterior/controller. Reuse the exact three S20 terminal science classes:
- M0 baseline-linear;
- M1 nonlocal-linear;
- M2 nonlocal-tanh.

For a fixed evidence temperature `tau`, compute class weights
`w_i(tau) = softmax(tau * log_evidence_i)`
and terminal DAG posterior
`p_tau = sum_i w_i(tau) p_i`.

`tau=1` reproduces S20 raw evidence weighting. `tau=0` is uniform posterior pooling. No abstention or per-world threshold is allowed.

## Training selection
Fresh training seeds 70101-70124 (n=24). Frozen grid:
`tau in {0.00, 0.02, 0.05, 0.10, 0.25, 0.50, 1.00}`.

For each tau record mean edge delta and Brier delta versus the unchanged planning control, large harms > +0.50, and mean class weights.

A candidate qualifies only if:
- mean edge delta vs planning control <= -0.10;
- mean Brier delta vs planning control <= +0.005;
- <= 3/24 large harms;
- exact planning-trace identity and all posterior normalization invariants.

Select the qualifying tau with lowest mean edge error. Ties within 0.01 edge-error units select the larger tau (retain more evidence information). Persist the complete training grid and selected tau before validation exposure.

## Validation
Fresh seeds 70201-70224 (n=24). The frozen selected tau passes only if:
- mean edge delta <= -0.10;
- mean Brier delta <= +0.005;
- <= 3/24 large harms;
- exact planning-trace identity and normalized posterior.

## Held-out confirmation
Only if validation passes: seeds 70301-70348 (n=48). Promotion requires:
- mean edge delta <= -0.10;
- paired bootstrap 95% upper bound < 0;
- mean Brier delta <= +0.005;
- <= 5/48 large harms;
- 100% coverage;
- exact planning-trace identity and normalized posterior.

## Controls
Report raw-evidence S20 (`tau=1`), uniform pooling (`tau=0`), baseline planning posterior, and frozen S5 nonlocal-linear posterior where useful. Resource/intervention budgets remain identical because aggregation occurs only after the completed baseline planning trace.

## Redirect rule
If no temperature qualifies or the frozen temperature fails validation/confirmation, do not tune tau on exposed worlds. Diagnose whether robust pooling should operate at edge-marginal level, use predictive stacking on separately held-out rows, or introduce a heavy-tail likelihood class. Any successor must change aggregation representation or likelihood, not return to abstention gates.
