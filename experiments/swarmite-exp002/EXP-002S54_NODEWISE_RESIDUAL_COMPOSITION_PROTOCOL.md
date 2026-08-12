# EXP-002S54 — Nodewise Residual-Process Posterior Composition

## Motivation
S52 showed that observable residual-state features can discriminate specialist wins, but hard graph-level selection selected no specialist worlds. S53 then falsified continuous graph-level averaging at training. The next justified change is representation granularity, not another graph-level threshold, cap, or temperature.

## Hypothesis
Residual-process mismatch is localized by target node. A nodewise observable residual-state model can identify where the heteroskedastic specialist is locally useful, mix S30 and P_HET edge marginals only for those target nodes, and reconstruct a DAG posterior from the resulting local edge probabilities. This can capture specialist headroom without imposing specialist mass on unaffected nodes.

## Frozen architecture
- Planning: unchanged baseline planner, intervention budget 15.
- Outer promotion/adjudication: frozen S46 continuous-risk gate.
- Anchor: frozen S30 posterior.
- Specialist: frozen S49 heteroskedastic-likelihood posterior.
- Candidate DAG universe and metrics: frozen benchmark v2.
- No graph-level cap/temperature grid and no hard specialist selector.
- Validation and confirmation ground truth remain unopened until preceding gates pass.

## Nodewise observable representation
For each target node, construct cross-fitted residual diagnostics using only accumulated terminal data:
1. log residual variance;
2. corr(log1p(|fitted|), |residual|);
3. log residual-variance slope versus log1p(|fitted|);
4. high/low fitted-magnitude log variance ratio;
5. standardized tail fraction |z|>2;
6. mean |z|;
7. binned log-variance dispersion;
8. intervention count on that target;
9. usable residual sample count.

On training worlds only, fit two ridge-regularized node models: logistic probability that P_HET has lower incoming-edge error than S30, and linear predicted local gain. Inputs are standardized from training only.

## Terminal composition
For target node v:
`w_v = p_win_v * clip(pred_gain_v / 0.25, 0, 1)`.
For each candidate incoming edge u→v:
`m_uv = (1-w_v) * m30_uv + w_v * mhet_uv`.
Reconstruct a DAG posterior with the normalized Bernoulli pseudo-likelihood over the frozen DAG set:
`log P54(G) = Σ_edges [I_G log(m_uv) + (1-I_G) log(1-m_uv)]`.

This is local posterior composition. It is materially different from S50/S53 whole-graph mixtures and S52 hard selection.

## Prospective splits
Fresh external-seed namespaces, disjoint from S53:
- Mechanics: 2 linear + 2 heteroskedastic.
- Training: 64 linear + 64 heteroskedastic.
- Validation: 32 linear + 32 heteroskedastic.
- Held-out confirmation: 64 linear + 64 heteroskedastic.

## Matched control
Frozen S46 outer gate with S30 terminal posterior on identical worlds, traces, interventions, RNG-isolated data, and budget.

## Metrics
- paired hybrid terminal edge-error difference P54 minus control;
- bootstrap 95% interval;
- hybrid Brier delta;
- promoted large harms (>0.50 edge-error increase);
- linear and heteroskedastic regime-specific paired differences;
- mean node specialist mass overall/by regime;
- node specialist-win AUC and Brier;
- unchanged outer coverage and trace identity.

## Training qualification
All must hold:
1. mechanics/trace identity pass;
2. mean node specialist mass in [0.005, 0.20];
3. candidate hybrid mean edge delta <= control + 0.01;
4. heteroskedastic candidate edge delta <= control - 0.02;
5. linear candidate edge delta <= control + 0.02;
6. candidate promoted large harms <= control;
7. candidate hybrid mean Brier delta <= 0.005;
8. node specialist-win AUC >= 0.60 and Brier <= constant-prevalence Brier.

## Validation qualification
Training criteria plus paired mean edge difference <= 0 and heteroskedastic paired mean difference <= -0.01.

## Confirmation success
Validation criteria plus bootstrap 95% upper bound < 0, no increase in promoted large harms, and heteroskedastic paired mean difference < -0.02.

## Falsification redirects
- Training failure with node AUC < 0.60: observable nodewise adjudication is inadequate; next experiment must change residual-process representation or likelihood class.
- Training failure with node AUC >= 0.60 but no structural gain: local composition rule is inadequate; next experiment should model posterior uncertainty over residual-process classes rather than retune this rule.
- Validation/confirmation failure: preserve as negative transfer and test explicit residual-process class uncertainty.
- Confirmation success: freeze S54 and run breadth transfer without retuning.
