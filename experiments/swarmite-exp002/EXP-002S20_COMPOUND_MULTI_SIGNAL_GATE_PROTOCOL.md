# EXP-002S20 — Multi-Signal Abstention Under Compound Shift

## Status
RUNNING after protocol freeze.

## Hypothesis
S19 shows D<=1.50 alone is structurally robust but slightly under-detects calibration risk when nonlinear mechanisms, heavy-tailed noise, and latent confounding occur together. A second model-check signal, residual dependence R, may identify the extra calibration-risk tail without changing planning or terminal inference.

## Frozen architecture
Use exact S19 compound worlds and architecture. Keep D<=1.50 fixed. Compute residual-dependence score R exactly as in S18 from observational-row residual correlations under the baseline MAP DAG. Promote only if D<=1.50 and R<=R_threshold; otherwise abstain. Neither signal affects planning.

## Training
Fresh seeds 69901-69924. Candidate R thresholds {0.20,0.25,0.30,0.35,0.40,0.50,infinity}. Passing thresholds require coverage>=0.50, promoted mean edge delta<=-0.10, promoted mean Brier delta<=+0.005, and <=2 promoted large harms. Select highest coverage; frozen tie-break chooses the smaller finite R threshold when coverage ties.

## Validation
Fresh seeds 70001-70024. Pass if coverage>=0.50, promoted mean edge delta<=-0.10, promoted mean Brier delta<=+0.005, <=2 promoted large harms, and trace identity.

## Confirmation
If validation passes, seeds 70101-70148. Require coverage>=0.50, promoted mean edge delta<=-0.10, bootstrap 95% upper bound<0, promoted mean Brier delta<=+0.005, <=4 promoted large harms, and trace identity.

## Redirect
If falsified, simple threshold stacking is insufficient under compound shift; redirect toward learned model-shift scoring or explicit ensemble uncertainty rather than further manual threshold additions.