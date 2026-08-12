# EXP-002S58 — Intervention-Conditional Residual-Process Likelihood

## Status
PREREGISTERED / FROZEN BEFORE PROSPECTIVE WORLDS

## Scientific redirect
S56 and S57 both generated strong variance-process evidence but harmed heteroskedastic structural inference. Replacing Gaussian with fixed Student-t residuals improved linear behavior but did not repair the heteroskedastic failure. The repeated failure points away from tail sensitivity and toward the fitted-magnitude slope representation itself.

## Hypothesis
Residual-scale instability is better represented by observable intervention/noise state than by fitted-signal magnitude. A partially pooled residual-scale likelihood conditional on intervention context can capture regime-local noise instability without distorting parent-set evidence in linear worlds.

## Frozen controls
- Baseline planner and intervention budget <= 15 unchanged.
- Frozen S30 terminal anchor.
- Frozen S46 outer promotion gate.
- Strong matched control is S46 + S30 on identical worlds/traces.
- No S56/S57 gamma or likelihood retuning.

## Candidate mechanism
For each target node and candidate parent set:
1. Fit the benchmark mean model and exclude samples directly intervening on the target node, exactly as prior terminal likelihoods do.
2. Treat the remaining intervention target identity as an observable residual-state label (including observational/no-target state).
3. Use a fixed Student-t residual model with nu=4.
4. Estimate one global robust residual scale.
5. Estimate a context-specific residual scale for each observed intervention state, shrunk toward the global log scale by fixed empirical-Bayes weight n_g/(n_g+5).
6. Score the context-conditional robust likelihood against the global robust likelihood with a fixed complexity penalty of 0.5*log(n) per effective extra context scale.
7. Add the clipped likelihood-evidence difference to that node/parent family score and reconstruct a normalized DAG posterior directly.

There is no graph-level mixture, nodewise posterior blend, learned gate, fitted-magnitude variance slope, or validation tuning.

## Prospective namespaces
- Mechanics: 2 linear + 2 heteroskedastic fresh worlds.
- Training: 64 + 64 fresh worlds.
- Validation: 32 + 32, unopened unless training qualifies.
- Held-out confirmation: 64 + 64, unopened unless validation qualifies.

## Qualification
Matched S46/S30 gates remain deliberately strict:
- candidate hybrid mean edge delta <= control + 0.01;
- heteroskedastic candidate <= control - 0.02;
- linear candidate <= control + 0.02;
- promoted large harms <= control;
- hybrid Brier delta <= 0.005;
- mean absolute family-score adjustment >= 0.02.
Validation additionally requires paired overall <= 0 and heteroskedastic <= -0.01.
Confirmation additionally requires paired bootstrap upper 95% < 0 and heteroskedastic paired difference < -0.02.

## Redirects
- If intervention-context evidence is nontrivial but harmful: move to a diagnostic decomposition of residual-state evidence versus parent-set ranking before another likelihood family.
- If evidence collapses: test residual autocorrelation/local dispersion state rather than intervention identity.
- If supported: freeze S58 and breadth-test without retuning.

Scientific falsification is a valid completed result.