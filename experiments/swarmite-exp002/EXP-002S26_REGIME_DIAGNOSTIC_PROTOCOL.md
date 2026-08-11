# EXP-002S26 — Heterogeneous Transfer Regime Diagnostic

Status: RUNNING after protocol freeze.

## Rationale
S25 had favorable overall edge error but failed preregistered regime guardrails. Its 4-world-per-regime screen suggested that the frozen S23 posterior remains beneficial under softsign+t5 and arctan+Laplace but can harm linear-Gaussian worlds; the tanh+t3 subset was too small and inconsistent with the much larger positive S23 result. Do not change the robust inference until these regime effects are resolved on larger fresh samples.

## Frozen diagnostic design
Use the exact S25 environment family and frozen S23 terminal inference. Fresh seeds 71000-71095 produce 96 worlds, exactly 24 per `seed mod 4` regime:
- linear_gaussian;
- tanh_t3;
- softsign_t5;
- arctan_laplace.

This is diagnostic only; no policy is promoted or tuned on these worlds.

## Per-world measurements
Record paired terminal edge/Brier deltas of frozen S23 inference versus baseline planning control, large harms, and the secondary S5 comparison. In addition record observable terminal mismatch signals computed without truth:
- `D_robust`: total absolute edge-marginal disagreement between frozen robust and planning posteriors;
- `PPC_tail` and `PPC_nonlinear` from the frozen S19 residual diagnostic applied to the terminal planning posterior.

Ground truth is used only for diagnostic performance stratification.

## Regime conclusions
For each regime report n=24, mean edge delta, paired bootstrap 95% CI, mean Brier delta, wins, large harms, and mean observable mismatch signals.

Label a regime `ROBUST_SUPPORTED` if mean edge delta < 0, bootstrap upper bound < 0, and mean Brier delta <= +0.005.
Label it `ROBUST_HARMFUL` if mean edge delta > 0 and bootstrap lower bound > 0, or mean Brier delta > +0.015.
Otherwise label it `UNRESOLVED`.

## Successor logic
- If linear-Gaussian is harmful while shifted regimes are supported, next test an observable model-class selector between baseline and robust science posteriors, with separate training/validation/confirmation and no ground-truth inputs at deployment.
- If tanh+t3 is not supported, reconcile the discrepancy against S23 before any selector work.
- If multiple shifted regimes are harmful, return to model-class expansion/representation rather than gating.

Do not modify S23 itself during this diagnostic.
