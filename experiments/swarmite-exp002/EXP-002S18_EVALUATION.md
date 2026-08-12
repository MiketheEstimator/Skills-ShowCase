# EXP-002S18 Evaluation — Multi-Signal Posterior-Disagreement Gate

## Disposition
`COMPLETE_FALSIFIED_ON_VALIDATION`

S18 tested whether three internal planning-vs-science disagreement signals could repair the compound-shift calibration failure seen in S17 without retuning the exposed one-dimensional threshold.

Training selected the highest-coverage qualifying gate: `D_sum <= 2.0`, `D_max <= 0.45`, and `science_entropy / planning_entropy >= 0.35`. It promoted all 24 training worlds with mean edge delta -0.535, mean Brier delta +0.00169, 23/24 wins, and zero large harms.

On fresh validation seeds 69401-69424, the frozen gate again promoted all 24 worlds and retained strong structural improvement: mean edge delta -0.495, 22/24 wins, zero large harms, and exact planning-trace identity. However mean Brier delta worsened to +0.00628, breaching the preregistered +0.005 calibration guardrail. Held-out confirmation was therefore not opened.

## Interpretation
The failure is informative. Posterior-to-posterior disagreement geometry alone, even enriched with maximum edge disagreement and entropy collapse, does not reliably detect the calibration failure created by simultaneous functional-form and noise-distribution mismatch. The next detector should include evidence about how poorly the planning model predicts the observed data, not only how two posteriors disagree.

## Next uncertainty
Test an observable posterior-predictive residual shift detector, combined with the supported structural disagreement signal, using fresh train/validation/held-out worlds. Do not retune S18 on exposed validation worlds.