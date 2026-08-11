# EXP-002S14 — Temperature-Calibrated Science Posterior

## Status
RUNNING after protocol freeze.

## Hypothesis
S10 and S13 show that the frozen nonlocal science posterior continues to improve structural edge recovery under nonlinear mechanism shift but becomes overconfident enough to violate Brier calibration. A posterior-temperature calibration layer may preserve the ranking/structural advantage while reducing overconfidence, without changing planning or model family.

## Frozen treatment family
Use the exact S10 nonlinear worlds, baseline planner, observations, and frozen nonlocal terminal posterior `p`. Apply only a terminal temperature transform `p_tau ∝ p^tau` with tau in {0.25, 0.50, 0.75, 1.00}. Tau=1.00 is S10. No transformed posterior may influence planning.

## Training and selection
Fresh training worlds 68101-68124. Evaluate all four tau values on identical worlds/traces. Select the tau with lowest mean Brier score subject to mean edge delta versus baseline <= -0.10 and <=3/24 worlds worsening edge error by >0.50. If multiple tau values have mean Brier within 0.001, choose the larger tau to preserve structural concentration. Persist the full grid and selected tau before validation.

## Validation
Fresh worlds 68201-68212. Pass if selected tau has mean edge delta <= -0.10, mean Brier delta <= +0.005, <=2/12 large harms, and exact planning-trace identity.

## Held-out confirmation
Only if validation passes, run 68301-68324. Promotion requires mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, <=3/24 large harms, and exact trace identity.

## Falsification redirect
If temperature calibration fails, preserve the structural benefit as real but insufficiently calibrated under nonlinear shift and redirect toward explicit uncertainty-aware abstention/reporting rather than more posterior reshaping.