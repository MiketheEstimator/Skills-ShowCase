# EXP-002S50 — Bounded World-Model Mixture Terminal Inference

## Motivation
EXP-002S49 falsified a fixed fitted-magnitude heteroskedastic terminal likelihood specialist at training. Even its weakest fixed blend improved heteroskedastic worlds but damaged the linear anchor and increased large harms. Earlier S33–S37 work also showed that unconstrained predictive weighting across a broad model set dilutes the robust S30 anchor and that S30 is the only safe global anchor. The unresolved hypothesis is therefore not that one specialist should replace S30, but that explicit uncertainty over a small set of terminal world models can allocate limited specialist mass only when observable evidence supports model mismatch.

## Hypothesis
A hierarchical two-world-model terminal mixture, with S30 as a mandatory anchor and a heteroskedastic likelihood specialist receiving only bounded per-world mass according to cross-fitted observable variance-model evidence, can recover some heteroskedastic benefit without the linear-anchor harms of S49.

## Material distinction from prior failures
- Not S33: no unconstrained seven-class softmax and no generic predictive-score weighting across mechanism classes.
- Not S35: no global structural stacking weights.
- Not S46/S48: no abstention or promotion threshold is changed.
- Not S49: specialist weight is not a fixed beta; it is a per-world latent model probability derived from out-of-sample variance-model evidence and is bounded by an anchor floor.
- Planning remains unchanged and baseline-only.

## Frozen architecture
- Planning: benchmark-v2 baseline posterior only, budget 15.
- Science anchor: exact S30 posterior.
- Alternate world model: exact S49 heteroskedastic terminal posterior.
- Adjudication: frozen S46 coefficients and promotion rule; S50 does not change who is promoted.
- If S46 does not promote, output the baseline posterior.
- If S46 promotes, output the S50 terminal mixture.
- Ground-truth DAG, regime label, realized edge error, and realized harm are evaluation-only and never enter deployment computation.

## Observable world-model evidence
After the fixed planning trajectory, compute 5-fold cross-fitted predictive evidence comparing two variance worlds while holding the mean-family selection mechanism fixed:
1. On each fold and node, fit all homoskedastic Gaussian parent families on training rows and select the highest training family score.
2. For the selected family, fit its Bayesian linear mean model on training rows.
3. Homoskedastic world: score held-out residuals under one training residual variance.
4. Heteroskedastic world: on training residuals fit `log(residual^2 + 0.05) = a + b*log1p(abs(fitted_mean))` with ridge 1.0; score held-out residuals under the resulting clipped variance function.
5. Sum held-out log scores across nodes/folds and divide the heteroskedastic-minus-homoskedastic difference by the number of scored observations.

Let `d_var` be this mean log-score advantage. Convert it to an observable latent world-model probability `q_het = sigmoid(d_var)`. No regime label is used.

## Bounded mixture
For cap `c`, define specialist mass `w = c * q_het` and
`P50(c) = (1-w)*P_S30 + w*P_HET`, normalized.

Training-only cap grid: `{0.10, 0.20, 0.30, 0.40}`. Therefore S30 always retains at least 60% posterior mass even under maximal heteroskedastic evidence.

## Training qualification
Use fresh balanced training worlds: 48 linear + 48 heteroskedastic. Frozen S46 controls promotion exactly as before.

A cap qualifies only if:
- mechanics hold and all posterior sums are finite;
- S46 promotion coverage >= 0.50;
- overall hybrid mean edge delta versus baseline < 0;
- heteroskedastic hybrid mean edge delta < 0;
- linear-anchor hybrid mean edge delta <= +0.02;
- overall and heteroskedastic promoted large-harm rate <= 0.05;
- hybrid mean Brier delta <= +0.005;
- at least 70% of frozen-S46/S30 overall structural improvement is retained;
- heteroskedastic hybrid edge delta is no worse than frozen S46/S30 by more than 0.02.

Choose the qualifying cap with the best heteroskedastic hybrid edge delta. Ties within 0.01 choose the smaller cap. Persist the selected cap before validation exposure.

## Prospective splits
- Mechanics: 4 fresh worlds, 2 linear + 2 heteroskedastic.
- Training: 96 fresh worlds, 48 + 48.
- Validation: 48 fresh worlds, 24 + 24.
- Held-out confirmation: 96 fresh worlds, 48 + 48, exposed only after validation success.

## Validation success
Require all training qualification criteria, at least 65% frozen-S46 improvement retention, and no mechanics violation.

## Confirmation promotion
Require validation criteria plus:
- paired bootstrap 95% upper bound for hybrid edge delta < 0;
- overall and heteroskedastic promoted large-harm rate <= 0.05;
- linear-anchor hybrid edge delta <= +0.02;
- heteroskedastic hybrid edge delta <= frozen S46/S30 heteroskedastic edge delta + 0.02;
- at least 65% frozen-S46 overall improvement retention.

## Falsification redirect
If S50 fails, reject bounded evidence-weighted S30/P_HET world-model averaging. Do not retry with another cap, temperature, or variance threshold. Redirect to a changed world-model mechanism, preferably a residual-process model that changes representation (for example latent variance state or nonparametric residual model), or to a diagnostic proving whether heteroskedastic breadth harm is primarily posterior-point-estimate failure versus adjudication failure.