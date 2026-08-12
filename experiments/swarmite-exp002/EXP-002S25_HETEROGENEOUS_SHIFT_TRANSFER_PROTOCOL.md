# EXP-002S25 — Frozen Robust Inference Across Heterogeneous Mechanism/Noise Regimes

Status: RUNNING after protocol freeze.

## Rationale
S23 supported the frozen tanh+t3 robust structural likelihood on the compound benchmark, and S24 transferred it without retuning to softsign+t5. The next test is whether one fixed terminal science model remains useful when the true mechanism/noise regime varies from world to world rather than staying homogeneous across an evaluation batch.

## Frozen treatment
Use the exact S23 terminal inference unchanged: tanh-parent regressors, Student-t nu=3 scale=1/sqrt(3), TAU2=4 ridge prior, deterministic IRLS, and the same complexity penalty. Preserve the baseline Gaussian planning posterior/controller, budget, proposals, and RNG isolation. No science quantity affects planning.

## Heterogeneous world regimes
Assign each seed deterministically by `seed mod 4` to one of four true environments:
0. `linear_gaussian`: original benchmark-v2 linear mechanism with Gaussian noise;
1. `tanh_t3`: S17 tanh mechanism with unit-variance Student-t(3) noise;
2. `softsign_t5`: S24 softsign mechanism with unit-variance Student-t(5) noise;
3. `arctan_laplace`: `arctan(parent)` mechanism with unit-variance Laplace noise (scale=1/sqrt(2)).

The treatment never receives the regime label.

## Mechanics
Seeds 70800-70803, exactly one world per regime. Require exact DAG support, spend <=15, planning reconstruction, finite scores, normalized posterior, and unchanged planning trace.

## Screen
Seeds 70804-70819 (n=16, four per regime). Advance only if:
- overall mean edge delta <= -0.10;
- overall mean Brier delta <= +0.005;
- <=3/16 large harms >+0.50;
- every regime mean edge delta <= +0.15;
- every regime mean Brier delta <= +0.015;
- all mechanics invariants.

## Held-out confirmation
Only if screen passes: seeds 70900-70947 (n=48, twelve per regime). Heterogeneous transfer is supported only if:
- overall mean edge delta <= -0.10;
- paired bootstrap 95% upper bound <0;
- overall mean Brier delta <= +0.005;
- <=6/48 large harms;
- no regime mean edge delta > +0.10;
- no regime mean Brier delta > +0.010;
- 100% coverage and all mechanics invariants.

## Reporting
Report overall and regime-stratified edge/Brier deltas, wins, harms, and bootstrap interval. S5 nonlocal-linear remains a secondary comparator.

## Redirect
If the fixed robust model fails only in one regime, diagnose/adapt to that model-class shift without changing successful regimes. If it succeeds across all regimes, promote robust terminal likelihood as the new reference science posterior and next test scale/open-world transfer rather than further synthetic parameter tuning.
