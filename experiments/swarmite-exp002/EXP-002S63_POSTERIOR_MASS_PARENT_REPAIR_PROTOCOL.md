# EXP-002S63 — Posterior-Mass Counterfactual Parent-Family Repair

## Status
Prospective protocol frozen before mechanics/training inspection.

## Basis
S61 showed that predictive-state error localization remained useful but its minimum-held-out-loss competitor proposal was wrong-direction on most anchor-error nodes (29.28% useful). S62 materially changed the proposal representation to intervention-conditioned local posterior disagreement and passed its diagnostic gate: best AUC 0.695745 (bootstrap 95% 0.657149–0.737155) and competitor usefulness 59.35% on anchor-ranking-error nodes. Because S61 failed the targeting/proposal gate rather than establishing a failure of the bounded correction geometry itself, S63 reuses that preregistered correction geometry with the independently supported S62 proposal.

## Hypothesis
A bounded structural posterior tilt toward the S62 posterior-mass competitor, activated only to the degree that an S62-feature model predicts anchor local-ranking error, will improve the frozen S46/S30 hybrid without increasing promoted large harms.

## Frozen inference construction
For each node:
1. Compute the S62 leave-one-state-out local posterior-disagreement features and nominated parent-family competitor using observable data only.
2. Fit one ridge-regularized logistic error-localization model on the fresh training panel using the eight S62 features. Ground truth is used only to fit this prospective training model and to evaluate held-out outcomes.
3. Continuous activation is frozen as in S61: `a = clip((p_error - train_prevalence)/(1-train_prevalence), 0, 1)`.
4. Proposal reliability uses the S62 nominated competitor's mean posterior mass relative to the uniform legal-family baseline: `r = clip((q_comp - 1/K)/(1 - 1/K), 0, 1)` where K is the number of legal local families.
5. Local tilt is frozen at `lambda_v = 0.75 * a * r`.
6. Apply the S61 local-family exponential posterior tilt to S30: DAGs matching the nominated S62 competitor at node v receive `+lambda_v`; DAGs matching the anchor-selected local family receive `-lambda_v`; normalize exactly.

No cap, temperature, threshold, amplitude, or proposal grid may be searched. Validation and confirmation are never used for fitting.

## Frozen controls
- baseline planner and budget 15 unchanged;
- S30 anchor unchanged;
- S46 outer promotion/adjudication unchanged;
- candidate and control use identical baseline traces and identical outer S46 promotion masks;
- control is S30 on promoted worlds and baseline otherwise.

## Prospective panels
- mechanics: 2 linear + 2 heteroskedastic worlds beginning 95601;
- training: 64 + 64 worlds beginning 95701;
- validation: 32 + 32 worlds beginning 96101;
- held-out confirmation: 64 + 64 worlds beginning 96401.

## Primary outcomes
- paired hybrid mean edge-error difference, S63 minus frozen S46/S30;
- regime-specific paired edge differences;
- promoted large harms;
- hybrid Brier delta;
- nonzero correction fraction and mean local tilt;
- held-out error-localization AUC/Brier;
- truth-scored competitor usefulness on anchor-ranking-error nodes, diagnostic only.

## Training qualification
All must hold:
1. mechanics/reproducibility pass, spend <= 15, traces identical;
2. nonzero correction on 2%–60% of nodes;
3. candidate hybrid mean edge delta <= control + 0.005;
4. heteroskedastic candidate <= control - 0.01;
5. linear candidate <= control + 0.015;
6. candidate promoted large harms <= control;
7. candidate hybrid mean Brier delta <= control + 0.005;
8. error-localization AUC >= 0.60 and Brier <= constant-prevalence Brier;
9. S62 competitor usefulness on anchor-error nodes > 0.50.

## Validation qualification
Training gates plus overall paired mean edge difference <= 0, heteroskedastic paired difference <= -0.005, and no excess large harms.

## Confirmation qualification
Validation gates plus bootstrap 95% upper endpoint for overall paired edge difference < 0, heteroskedastic paired difference < -0.01, and no excess large harms.

## Disposition
- `SUPPORTED`: enqueue frozen breadth/transfer test without retuning.
- `FALSIFIED_TARGETING`: localization or S62 proposal usefulness fails prospectively; change representation/proposal, not thresholds.
- `FALSIFIED_CORRECTION_GEOMETRY`: localization and proposal remain supported but structural performance fails; change posterior correction geometry to constrained projection/replacement rather than tune lambda.
- `BLOCKED_EXECUTION_*`: repair only execution defects without opening later panels.

Scientific falsification is a valid completed result and triggers the next materially justified queue item immediately.