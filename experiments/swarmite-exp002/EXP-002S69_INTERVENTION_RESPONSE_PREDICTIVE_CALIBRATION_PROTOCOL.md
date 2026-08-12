# EXP-002S69 — Intervention-Response Predictive Calibration Diagnostic

## Hypothesis
The S66-S68 acquisition failures are caused materially by misspecified posterior-predictive intervention responses: simulated outcome branches are under/over-dispersed or biased relative to fresh realized intervention responses, so downstream disagreement and VOI scores cannot reliably rank acquisition value.

## Objective
Directly test calibration of the frozen benchmark posterior-predictive response generator before constructing any new planner score.

## Frozen components
- Baseline planner and budget remain unchanged.
- S30 remains the inference anchor.
- Existing `build_family_models`, `posterior_from_fs`, and `sim_row_from_posterior` define the predictive model under test.
- Actual intervention responses are generated only after target/setpoint selection using the benchmark environment; truth is scoring-only.
- No planner policy is promoted in S69.

## Prospective design
1. Mechanics: 2 fresh linear + 2 fresh heteroskedastic worlds.
2. Diagnostic: 64 fresh linear + 64 fresh heteroskedastic worlds.
3. For every world, target node, and setpoint {-2,+2}, draw 32 posterior-predictive response rows.
4. Generate one fresh realized environment response for the identical target/setpoint.
5. For each non-intervened response dimension measure predictive mean, predictive SD, standardized residual, 80% interval coverage, and 95% interval coverage.
6. Aggregate globally and separately by linear/heteroskedastic regime.

## Preregistered interpretation
Predictive calibration is `SUPPORTED` only if both regimes satisfy: absolute mean standardized residual <= 0.25, standardized-residual RMS in [0.75,1.35], 80% coverage in [0.70,0.90], and 95% coverage in [0.88,0.99]. If finite but any regime fails, disposition is `PREDICTIVE_MISCALIBRATION_SUPPORTED`. Nonfinite/invalid mechanics is execution-blocking, not scientific falsification.

## Successor logic
- If calibrated: redirect away from predictive misspecification and test non-scalar/set-valued acquisition utility using calibrated branches.
- If miscalibrated: localize bias/dispersion failure by regime and build a cross-fitted response-calibration layer before any planner policy test.
- Never retune S66-S68 scalar scores as the response to this diagnostic.
