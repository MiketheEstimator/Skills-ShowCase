# EXP-002S15 — Disagreement-Aware Structural Abstention

## Status
RUNNING after protocol freeze.

## Hypothesis
Across S10, S13, and S14, the dual-posterior science model retains strong structural edge-recovery gains under nonlinear shift, but full-posterior Brier calibration is unstable. Rather than reshaping the posterior again, Swarmite should detect internal model disagreement and abstain from high-confidence structural promotion when the planning posterior and science posterior diverge too strongly.

## Frozen architecture
Planning remains the benchmark-v2 linear Gaussian planner on nonlinear `tanh(parent)` worlds. Terminal inference computes both the baseline posterior and frozen S10 nonlocal science posterior. No terminal model may influence planning.

For each world compute the observable disagreement score `D = sum(abs(edge_marginals(nonlocal)-edge_marginals(baseline)))`. A world is `PROMOTE_NONLOCAL` when D <= threshold, otherwise `ABSTAIN_MODEL_SHIFT`. Abstention means the engine reports the structural result as unresolved/model-shift-sensitive rather than claiming the nonlocal posterior is calibrated.

## Training
Fresh seeds 68401-68424. Candidate thresholds are {0.50, 1.00, 1.50, 2.00, 3.00, infinity}. For each threshold report coverage, promoted-set mean edge delta, promoted-set mean Brier delta, large harms, and abstention rate. Select the highest-coverage threshold satisfying: coverage >= 0.50, promoted-set mean edge delta <= -0.10, promoted-set mean Brier delta <= +0.005, and <=2 promoted worlds with edge harm >0.50. If none qualifies, falsify the gate.

## Validation
Fresh seeds 68501-68524. Freeze the selected threshold before validation. Pass if coverage >=0.50, promoted-set mean edge delta <= -0.10, promoted-set mean Brier delta <= +0.005, <=2 promoted large harms, and exact planning-trace identity.

## Held-out confirmation
Only if validation passes: seeds 68601-68648. Promotion requires coverage >=0.50, promoted-set mean edge delta <= -0.10, bootstrap 95% upper bound <0 on promoted worlds, promoted-set mean Brier delta <= +0.005, <=4 promoted large harms, and exact trace identity.

## Interpretation boundary
This experiment does not claim abstained worlds are solved. Success means Swarmite can preserve the supported structural advantage where its internal models agree while explicitly surfacing mechanism-shift uncertainty elsewhere.