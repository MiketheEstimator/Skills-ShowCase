# EXP-002S13 — Model-Averaged Science Posterior Under Nonlinear Shift

## Status
RUNNING after protocol freeze.

## Hypothesis
S10 retained strong edge-recovery gains but violated the Brier guardrail; S11-S12 showed that switching terminal inference wholesale to an explicit nonlinear family is structurally harmful. A convex mixture of the baseline linear-Gaussian terminal posterior and the S10 linear-nonlocal terminal posterior may preserve structural gain while tempering S10 overconfidence under nonlinear misspecification.

## Frozen architecture
Planning remains exactly the S10 baseline linear-Gaussian planner on nonlinear `tanh(parent)` worlds. Terminal science posterior only is mixed as `p_mix(alpha)=(1-alpha)*p_baseline + alpha*p_nonlocal`, where `p_baseline` is the frozen benchmark-v2 posterior after the identical trace and `p_nonlocal` is the frozen S10/S5 terminal posterior. No mixture component may influence planning.

## Training and selection
Fresh training worlds: seeds 67801-67824. Evaluate alpha in {0.00,0.25,0.50,0.75,1.00}. Select the alpha with lowest mean edge error subject to mean Brier delta versus alpha=0 <= +0.005 and <=3/24 worlds worsening edge error by >0.50. Ties within 0.01 edge-error units choose the smaller alpha. Persist the full grid and frozen alpha before validation.

## Validation
Fresh seeds 67901-67912. Pass only if selected alpha vs alpha=0 has mean edge delta <= -0.10, mean Brier delta <= +0.005, <=2/12 large harms, and exact planning-trace identity.

## Held-out confirmation
Only if validation passes: fresh seeds 68001-68024. Promotion requires mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, <=3/24 large harms, and exact trace identity.

## Falsification redirect
If mixture averaging fails, preserve S10 as evidence that separation survives structurally but not calibrationally under mechanism shift, and redirect toward uncertainty-aware calibration or abstention rather than further terminal-family substitution.