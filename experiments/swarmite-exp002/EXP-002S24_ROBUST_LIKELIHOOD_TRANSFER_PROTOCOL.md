# EXP-002S24 — Frozen Robust-Likelihood Transfer Under Unseen Shift

Status: RUNNING after protocol freeze.

## Rationale
S23 strongly supported terminal inference using tanh-parent Student-t(3) robust quasi-evidence under the compound tanh + t3 stress model. The critical next question is whether that gain reflects a generally useful robustness mechanism or merely a close match to the synthetic generator.

## Frozen treatment
Do not retune any S23 inference parameter. Preserve:
- tanh(parent) treatment regressors;
- Student-t treatment likelihood nu=3, scale=1/sqrt(3);
- TAU2=4 ridge prior;
- 30 deterministic IRLS iterations maximum and 1e-8 tolerance;
- the same structural complexity penalty;
- exact baseline planning posterior/controller and budget.

## Unseen environment shift
Generate worlds with the same DAG/weight generator but replace the S17 environment by:
- causal mechanism `softsign(x)=x/(1+abs(x))` applied to parent values before the weighted sum;
- Student-t noise with nu=5 scaled to unit variance (`sqrt((nu-2)/nu)`).

This changes both nonlinear functional shape and tail thickness while preserving comparable variance and intervention semantics. The treatment remains frozen at its S23 tanh+t3 assumptions.

## Mechanics
Seeds 70601-70604. Require exact 29,281-DAG support, spend <=15, planning reconstruction, finite scores, normalized treatment posterior, and planning-trace identity.

## Prospective screen
Seeds 70611-70622 (n=12). Advance if mean edge delta <= -0.10, mean Brier delta <= +0.005, <=2 large harms >+0.50, and all mechanics invariants.

## Held-out confirmation
Only if screen passes: seeds 70701-70736 (n=36). Transfer is supported only if mean edge delta <= -0.10, bootstrap 95% upper bound <0, mean Brier delta <= +0.005, <=4 large harms, 100% coverage, and all mechanics invariants.

## Controls
Unchanged baseline planning posterior is primary control. Frozen S5 nonlocal-linear terminal posterior is a secondary comparator. No treatment quantity influences planning.

## Redirect
If transfer fails, preserve S23 as benchmark-specific supported evidence and diagnose which shift dimension (softsign mechanism versus t5 noise) causes loss. If transfer succeeds, advance to heterogeneous per-world mechanism/noise shift without retuning.
