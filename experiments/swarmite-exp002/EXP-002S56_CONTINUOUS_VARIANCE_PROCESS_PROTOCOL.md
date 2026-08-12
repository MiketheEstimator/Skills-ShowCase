# EXP-002S56 — Continuous Variance-Process Likelihood

## Status
PREREGISTERED / FROZEN BEFORE PROSPECTIVE WORLDS

## Scientific redirect
S55 showed prospective residual-class discrimination (node specialist-win AUC 0.6075) but its explicit binary anchor/heteroskedastic class marginalization worsened paired edge performance (+0.0554). The failure therefore does not justify retuning binary class probabilities. S56 changes the residual-process likelihood itself.

## Hypothesis
The remaining heteroskedastic failure is caused in part by representing residual processes as a binary anchor-vs-specialist class. Marginalizing a continuous variance-slope process within each target-node/parent-set likelihood will preserve model uncertainty while avoiding a hard two-class decomposition and improve heteroskedastic structural inference without materially damaging linear worlds.

## Frozen controls
- Planner/intervention trace: unchanged baseline planner, budget <= 15.
- Terminal anchor: frozen S30 posterior.
- Outer adjudication: frozen S46 promotion rule.
- Strong matched control: S46 + S30 under identical worlds/traces/resources.
- Diagnostic comparator: original S49 heteroskedastic posterior, not used for tuning.

## Candidate mechanism
For every target node and candidate parent set:
1. Fit the same mean model used by the benchmark family model.
2. Compute residuals on observations where that target was not intervened upon.
3. Let z = standardized log(1 + |fitted mean|).
4. Define log variance as log(sigma^2) + gamma*z.
5. Numerically marginalize gamma over a frozen grid from -1.5 to 2.5 with Gaussian N(0,1) prior weights.
6. For each gamma, profile sigma^2 analytically from residuals.
7. Convert the marginal variance-process evidence into an additive family-score adjustment relative to gamma=0, with the same finite clipping discipline used by the earlier heteroskedastic specialist.
8. Reconstruct one normalized DAG posterior directly from these adjusted family scores.

No graph-level posterior blending, nodewise edge-marginal blending, binary residual class, learned threshold, or validation retuning is permitted.

## Prospective namespaces
- Mechanics: 2 linear + 2 heteroskedastic fresh worlds.
- Training gate: 64 linear + 64 heteroskedastic fresh worlds.
- Validation: 32 + 32 fresh worlds, unopened unless training qualifies.
- Held-out confirmation: 64 + 64 fresh worlds, unopened unless validation qualifies.

## Metrics
Paired against frozen S46/S30:
- hybrid mean edge delta vs baseline;
- paired candidate-control edge difference and bootstrap 95% interval;
- hybrid mean Brier delta;
- promoted large harms;
- linear and heteroskedastic regime-specific paired differences;
- fraction and magnitude of family-score adjustments;
- candidate posterior normalization/mechanics.

## Training qualification
All must hold:
- mechanics valid and traces/resources matched;
- candidate hybrid mean edge delta <= control + 0.01;
- heteroskedastic candidate hybrid mean edge delta <= control - 0.02;
- linear candidate hybrid mean edge delta <= control + 0.02;
- candidate promoted large harms <= control promoted large harms;
- candidate hybrid mean Brier delta <= 0.005;
- nontrivial variance-process adjustment mass, with mean absolute score adjustment >= 0.02.

## Validation qualification
Training criteria plus:
- overall paired mean edge difference <= 0;
- heteroskedastic paired mean edge difference <= -0.01.

## Confirmation support
Validation criteria plus:
- upper bound of paired bootstrap 95% interval < 0;
- heteroskedastic paired mean edge difference < -0.02.

## Falsification redirects
- If adjustments are nontrivial but structural gains fail: next experiment tests a heavier-tailed/robust residual likelihood rather than retuning gamma.
- If adjustments collapse toward zero: next experiment expands the variance-process covariates beyond fitted magnitude.
- If supported: freeze S56 and test breadth transfer without retuning.

Scientific falsification counts as a completed experiment.