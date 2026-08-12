# EXP-002S57 — Robust Continuous Residual-Process Likelihood

## Status
PREREGISTERED / FROZEN BEFORE PROSPECTIVE WORLDS

## Scientific redirect
S56 produced large, nontrivial continuous variance-process evidence (mean absolute family-score adjustment about 0.995) yet worsened paired structural edge performance overall and especially in heteroskedastic worlds. Linear performance was approximately neutral. This falsifies the Gaussian continuous variance-process likelihood as implemented, not the existence of residual-process signal.

## Hypothesis
Gaussian residual scoring overreacts to high-leverage/tail residuals when estimating variance-process evidence, causing the structurally harmful S56 score shifts. A fixed heavy-tailed Student-t residual likelihood, while preserving the frozen S56 continuous variance-slope marginalization, will make variance-process evidence robust enough to improve heteroskedastic inference without harming linear worlds.

## Frozen controls and inherited choices
- Baseline planner/intervention trace unchanged, budget <= 15.
- Frozen S30 terminal anchor and frozen S46 outer promotion gate.
- Matched strong control: S46 + S30.
- S56 gamma grid is inherited unchanged: [-1.5, 2.5] with 17 points.
- Gamma prior remains N(0,1).
- No graph-level or nodewise posterior mixing.
- No threshold, temperature, gamma-grid, or degrees-of-freedom tuning on prospective worlds.

## Candidate mechanism
For each target node and candidate parent set:
1. Use the benchmark mean-model fit.
2. Standardize z = log(1 + |fitted mean|).
3. Define residual scale_i = s * exp(gamma*z/2).
4. Use a fixed Student-t likelihood with nu=4 degrees of freedom.
5. For each inherited gamma value, profile the positive base scale s deterministically over a frozen log-scale grid centered on a robust MAD/RMS scale estimate.
6. Numerically marginalize gamma with the inherited N(0,1) prior.
7. Compare the marginalized robust evidence with the gamma=0 robust evidence and add the clipped evidence difference to the benchmark family score.
8. Reconstruct one normalized DAG posterior directly from adjusted family scores.

## Prospective namespaces
- Mechanics: 2 linear + 2 heteroskedastic.
- Training: 64 + 64.
- Validation: 32 + 32, sealed unless training qualifies.
- Held-out confirmation: 64 + 64, sealed unless validation qualifies.

## Metrics and qualification
Use the exact S56 matched metrics and gates:
- candidate hybrid edge delta <= frozen control + 0.01;
- heteroskedastic candidate <= control - 0.02;
- linear candidate <= control + 0.02;
- candidate promoted large harms <= control;
- hybrid Brier delta <= 0.005;
- mean absolute family-score adjustment >= 0.02.
Validation additionally requires overall paired difference <= 0 and heteroskedastic paired difference <= -0.01.
Confirmation additionally requires bootstrap 95% upper bound < 0 and heteroskedastic paired difference < -0.02.

## Redirects
- If robust evidence is nontrivial but still structurally harmful: abandon fitted-magnitude variance slope as the primary residual-process representation and test intervention-conditional/noise-state structure.
- If robust evidence collapses: test richer variance covariates with robust likelihood.
- If supported: freeze S57 and run breadth transfer without retuning.

Scientific falsification is a completed result.