# EXP-002S46 — Continuous Observable Harm-Risk Prediction for Terminal S30

## Motivation
S45 rejected a discrete six-class decision ontology. Although its mechanism posterior beat uniform prediction, class-averaged harm estimates caused extreme over-abstention: validation coverage fell to 8.3% and only 5.0% of available S30 improvement was retained. The topology-only control retained the full structural benefit but still exposed occasional dense-cell harms. The unresolved problem is therefore per-world risk prediction, not further discrete class refinement.

## Hypothesis
A regularized continuous model using only observable posterior/model diagnostics can predict when terminal S30 is likely to help or harm well enough to preserve most structural benefit while keeping the promoted large-harm rate within 5%.

## Frozen planner and science anchor
- Planning remains benchmark-v2 baseline posterior only, budget 15.
- S30 remains terminal-only and identical to the committed S30/S43–S45 lineage.
- No S46 feature may use ground-truth DAG, true topology label, true mechanism label, or realized S30 edge error at deployment.

## Observable feature vector
Computed after the fixed planning trajectory:
1. S42 `p_dense` topology evidence.
2–4. Three S45 out-of-sample mechanism/noise predictive scores (`tanh`, `sin`, `asinh`).
5. S39 mean credal width.
6. S30 LG-vs-TT mixture weight `alpha`.
7. Baseline posterior entropy.
8. S30 posterior entropy.
9. Mean absolute edge-marginal change from baseline to S30.
10. Maximum absolute edge-marginal change from baseline to S30.
11. Baseline maximum DAG posterior mass.
12. S30 maximum DAG posterior mass.
13. Baseline expected edge count.
14. S30 expected edge count.

The model also includes prespecified continuous interactions `p_dense × {three mechanism scores, credal width, alpha}`. All features are standardized using training means and standard deviations only.

## Prediction models
Two fixed L2-regularized linear models are trained on fresh training worlds:
- Ridge regression (`lambda=2.0`) predicts continuous S30 edge delta versus baseline.
- Logistic regression (`lambda=2.0`, deterministic IRLS, maximum 50 iterations) predicts the probability of a large harm (`edge delta > +0.50`).

No model architecture or regularization strength is selected using validation or confirmation worlds.

## Frozen promotion-rule selection
On training worlds only, evaluate the Cartesian grid:
- predicted-edge cutoff in `{-0.50, -0.25, -0.10, 0.00, +0.10}`;
- predicted-harm cutoff in `{0.05, 0.10, 0.20, 0.30}`.

Promote S30 iff both predicted edge delta <= edge cutoff and predicted harm probability <= harm cutoff.

A candidate qualifies on training only if:
- coverage >= 0.40,
- realized promoted large-harm rate <= 0.05,
- hybrid mean edge delta < 0,
- hybrid mean Brier delta <= +0.005,
- if always-S30 is beneficial, improvement retention >= 0.60.

Among qualifying candidates choose highest improvement retention; ties within 0.01 select lower harm cutoff, then lower edge cutoff. Persist the trained coefficients, standardization parameters, full rule grid, and selected rule before validation exposure.

## Prospective splits
All worlds remain the balanced S44 joint topology × heteroskedastic nonlinear family, but use fresh seeds:
- Training: 73801–73920 (120 worlds; 20 per joint cell).
- Validation: 74001–74060 (60 worlds; 10 per joint cell).
- Held-out confirmation: 74101–74220 (120 worlds; 20 per joint cell), exposed only after validation passes.

## Matched controls
On the same worlds report:
1. baseline,
2. always-S30,
3. frozen S43 topology-only decision,
4. frozen S39 scalar credal gate.

## Validation success
- mechanics and finite-feature invariants hold,
- coverage >= 0.40,
- promoted large-harm rate <= 0.05,
- hybrid mean edge delta < 0,
- hybrid mean Brier delta <= +0.005,
- if always-S30 is beneficial, improvement retention >= 0.60,
- continuous-risk hybrid retains at least 0.55 of the absolute benefit of the topology-only control,
- large-harm classifier Brier score <= the constant training-prevalence predictor Brier score on validation.

## Confirmation promotion
Require all validation criteria plus:
- paired bootstrap 95% upper bound for hybrid edge delta < 0,
- improvement retention >= 0.60,
- no joint cell with promoted large-harm rate > 0.10,
- overall promoted large-harm rate <= 0.05.

## Interpretation
Success supports observable continuous risk prediction as the uncertainty/adjudication layer around S30. Failure rejects this fixed low-capacity linear risk model and redirects to either nonlinear learned risk features or a broader posterior ensemble, not discrete class thresholds or hand-tuned topology gates.
