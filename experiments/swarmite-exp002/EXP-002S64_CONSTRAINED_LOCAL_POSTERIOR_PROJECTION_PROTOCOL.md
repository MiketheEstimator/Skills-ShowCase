# EXP-002S64 — Constrained Local Posterior Projection Repair

## Status
Prospective protocol frozen before mechanics/training inspection.

## Scientific basis
EXP-002S63 prospectively preserved the S62 evidence signal (error-localization AUC 0.712545; S62 proposal usefulness 0.605469 on anchor-ranking-error nodes) but its exponential `+lambda/-lambda` DAG tilt produced a slightly harmful paired edge difference (+0.002843). This is a correction-geometry falsification, not a localization/proposal falsification. S64 therefore preserves the S62 evidence and changes only how local evidence is converted into a globally valid DAG posterior.

## Hypothesis
The S63 failure is caused by forcing evidence through a two-family exponential tilt. Replacing that operation with a bounded projection toward the full intervention-state-refit local parent-family distribution can use S62's supported evidence while preserving uncertainty over multiple plausible parent families and avoiding overcommitment to one nominated competitor.

## Frozen components
- benchmark/data generator, DAG universe, baseline planner, budget 15, S30 anchor, and S46 outer adjudication remain unchanged;
- S62 leave-one-state-out local posterior construction remains unchanged;
- no S56-S58 residual likelihood, no S49 specialist, and no S63 exponential tilt is used;
- validation/confirmation are never used for fitting or choosing parameters.

## New correction geometry
For each target node v:
1. Compute the S30 posterior's induced local parent-family marginal `m30_v(pm)` over the legal parent masks.
2. Compute S62's mean leave-one-state-out local family posterior `q62_v(pm)` from observable intervention/noise-state refits.
3. Fit the same ridge-regularized error-localization model on the fresh training panel using the eight frozen S62 features.
4. Frozen activation: `a_v = clip((p_error - train_prevalence)/(1-train_prevalence), 0, 1)`.
5. Frozen reliability: Jensen-Shannon agreement-aware confidence `r_v = clip(competitor_mean_mass * (1 - mean_js), 0, 1)`.
6. Frozen projection fraction: `rho_v = 0.50 * a_v * r_v`.
7. Form a target local family distribution `t_v = (1-rho_v)*m30_v + rho_v*q62_v`.
8. Construct one globally valid DAG posterior by iterative proportional fitting (IPF) over the finite frozen DAG universe: cyclically rescale DAG mass so each activated node's local parent-family marginal approaches `t_v`, preserving support of S30. Stop at 40 cycles or maximum local-marginal error < 1e-8. Normalize exactly.

This is materially different from S63: S64 retains the entire set-valued S62 parent-family uncertainty and solves a constrained global marginal projection rather than rewarding one competitor and penalizing one anchor family.

## Fixed numerical safeguards
- S30 support floor before projection: 1e-300;
- target family floor: 1e-8 followed by normalization;
- IPF multiplicative ratio clip: [0.25, 4.0] per update;
- 40 fixed cycles maximum;
- no grid search over projection fraction, cycles, clips, or feature thresholds.

## Prospective panels
- mechanics: 2 linear + 2 heteroskedastic worlds beginning 96801;
- training: 64 + 64 worlds beginning 96901;
- validation: 32 + 32 worlds beginning 97301;
- held-out confirmation: 64 + 64 worlds beginning 97601.

## Matched control
Frozen S46 outer promotion decisions are applied identically. Control is S30 on promoted worlds and baseline otherwise. Candidate substitutes S64 only on the same promoted worlds. Planning trace, spend, and coverage must match exactly.

## Primary outcomes
- paired hybrid mean edge-error difference candidate minus frozen S46/S30;
- linear and heteroskedastic paired differences;
- promoted large harms;
- hybrid Brier delta;
- mean/nonzero projection fraction;
- final IPF marginal residual;
- held-out S62 error-localization AUC/Brier and proposal usefulness, retained as mechanism checks.

## Training qualification
All must hold:
1. mechanics pass, identical trace, spend <= 15, finite normalized posterior;
2. mean final IPF local-marginal residual <= 0.02;
3. nonzero projection on 2%-70% of nodes;
4. candidate hybrid mean edge delta <= control + 0.003;
5. heteroskedastic candidate <= control - 0.008;
6. linear candidate <= control + 0.012;
7. candidate promoted large harms <= control;
8. candidate hybrid Brier delta <= control + 0.005;
9. localization AUC >= 0.60 and Brier <= constant-prevalence Brier;
10. S62 proposal usefulness on anchor-error nodes > 0.50.

## Validation qualification
Training gates plus overall paired edge difference <= 0, heteroskedastic paired difference <= -0.004, and no excess large harms.

## Confirmation qualification
Validation gates plus bootstrap 95% upper endpoint for overall paired edge difference < 0, heteroskedastic paired difference < -0.008, and no excess large harms.

## Disposition and successor logic
- `SUPPORTED`: breadth/mechanism-shift transfer with the entire S64 mechanism frozen.
- `FALSIFIED_PROJECTION_GEOMETRY`: evidence checks remain supported but structural gates fail; next test must change the global consistency mechanism, e.g. decision-theoretic edge action or constrained MAP ensemble, not retune rho/IPF.
- `FALSIFIED_EVIDENCE_TRANSFER`: S62 evidence no longer passes prospectively; return to set-valued/invariance representation diagnostics, not projection tuning.
- `BLOCKED_EXECUTION_*`: repair only execution defects without opening later panels.

Scientific falsification is a completed result and immediately redirects the queue.