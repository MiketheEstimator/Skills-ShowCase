# EXP-002S61 — Bounded Predictive-State Targeted Structural Correction

## Status
Prospective protocol frozen before mechanics/training inspection.

## Motivation
EXP-002S60 found that truth-free leave-one-intervention-state-out predictive transport localizes frozen-anchor local parent-family ranking errors above chance. The strongest frozen feature, `cv_competitor_advantage`, reached AUC 0.652229 (bootstrap 95% 0.607183–0.693392). S56–S58 already falsified direct residual-likelihood substitution, while S52–S55 showed that simply gating or averaging previously defined specialists is insufficient. S61 therefore changes the corrective object itself: it uses predictive transport to nominate an alternative local parent family and applies only a bounded structural posterior tilt toward that alternative.

## Hypothesis
On nodes where cross-fitted intervention-state predictive transport indicates that the frozen anchor-selected parent family is unstable, the best truth-free counterfactual competitor can provide a useful local structural repair. A bounded posterior tilt toward that competitor will improve matched S46/S30 hybrid structural error without increasing promoted large harms.

## Frozen components
- Benchmark/data generator, candidate DAG universe, budget, and outer S46 promotion/adjudication are frozen.
- Baseline planning remains budget 15 and truth-blind.
- S30 remains the anchor posterior.
- S60 predictive features are computed exactly from observed data/intervention labels; ground truth is never used to construct a feature, select a competitor, or modify a posterior.
- Ground truth is permitted only for training the prospective error-localization model and for post-hoc scoring.

## New mechanism
For each target node:
1. Build the ordinary frozen local family score table and identify the anchor-selected local parent mask.
2. Perform the S60 leave-one-intervention-state-out predictive transport calculation for every legal local parent family.
3. Nominate the non-anchor family with the smallest mean held-out predictive loss as the counterfactual competitor.
4. Form the frozen S60 feature vector and fit one ridge-regularized logistic model on the training panel to predict whether the anchor local family is ranking-wrong.
5. Convert predicted error probability into a bounded continuous correction strength. No specialist posterior is reused and no threshold/cap grid is searched.
6. Tilt the S30 DAG posterior only through local-family agreement: DAGs whose incoming parent mask matches the nominated competitor receive positive bounded evidence; DAGs matching the anchor-selected family receive equal negative bounded evidence. Normalize exactly.

This differs materially from S52 hard selection, S53 graph-level averaging, S54 edge-marginal composition, S55 latent residual-class marginalization, and S56–S58 residual-likelihood substitution.

## Frozen correction rule
- Feature vector: S60 six predictive-state features plus `log1p(cv_competitor_advantage)` and anchor local-score gap.
- Logistic ridge penalty: 5.0.
- Training prevalence is retained for calibration diagnostics.
- Continuous activation: `a = clip((p_error - prevalence) / max(1-prevalence, 1e-6), 0, 1)`.
- Evidence reliability: `r = clip(log1p(cv_competitor_advantage) / log(3), 0, 1)`.
- Local tilt amplitude: `lambda_v = 0.75 * a * r`.
- No parameter grid, threshold search, or validation retuning is allowed.

## Prospective panels
Use fresh disjoint external-seed namespaces:
- mechanics: 2 linear + 2 heteroskedastic worlds beginning 94101;
- training: 64 + 64 worlds beginning 94201;
- validation: 32 + 32 worlds beginning 94601;
- held-out confirmation: 64 + 64 worlds beginning 94901.

Validation and confirmation remain unopened unless every preceding gate passes.

## Matched control
For every world use the frozen S46 outer promotion decision. The matched control is S30 when S46 promotes and the baseline posterior otherwise. The S61 candidate substitutes the corrected posterior only on those same frozen promoted worlds. Thus planning trace, spend, and outer coverage are identical between control and candidate.

## Primary outcomes
- paired hybrid mean edge-error difference, candidate minus frozen S46/S30;
- heteroskedastic and linear paired differences separately;
- promoted large harms (`edge_delta > 0.50`);
- hybrid Brier delta;
- mean local correction mass/amplitude and fraction of nodes with nonzero correction;
- error-localization AUC/Brier of the frozen training model;
- truth-scored competitor usefulness, reported diagnostically only.

## Training qualification gate
All must hold:
1. mechanics/reproducibility pass and identical baseline traces/spend <= 15;
2. nonzero correction on at least 2% but no more than 60% of nodes;
3. candidate hybrid mean edge delta <= control + 0.005;
4. heteroskedastic candidate hybrid mean edge delta <= control - 0.01;
5. linear candidate hybrid mean edge delta <= control + 0.015;
6. candidate promoted large harms <= control promoted large harms;
7. candidate hybrid mean Brier delta <= control + 0.005;
8. error-localization AUC >= 0.60 and Brier <= constant-prevalence Brier;
9. nominated competitor is truth-scored better than the anchor-selected family on > 50% of anchor-ranking-error nodes. This is an evaluation-only criterion, not an inference input.

## Validation qualification
Training gates plus:
- overall paired mean edge difference <= 0;
- heteroskedastic paired mean edge difference <= -0.005;
- no excess promoted large harms.

## Confirmation qualification
Validation gates plus:
- upper endpoint of bootstrap 95% CI for overall paired mean edge difference < 0;
- heteroskedastic paired mean edge difference < -0.01;
- no excess promoted large harms.

## Disposition and successor logic
- `SUPPORTED`: proceed to S62 breadth/transfer confirmation without retuning.
- `FALSIFIED_TARGETING`: if error localization AUC < 0.60 or competitor usefulness <= 50%, change representation/proposal mechanism; do not tune S61 activation.
- `FALSIFIED_CORRECTION_GEOMETRY`: if localization and competitor usefulness pass but structural gates fail, retain predictive-state evidence and test posterior projection/constrained local replacement rather than tilt-strength tuning.
- `BLOCKED_EXECUTION_*`: repair only the execution defect without exposing unopened panels.

Scientific falsification is a completed result and immediately triggers the materially appropriate successor.