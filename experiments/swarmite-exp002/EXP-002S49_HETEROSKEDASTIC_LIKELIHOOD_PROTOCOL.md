# EXP-002S49 — Heteroskedastic Terminal-Likelihood Specialist

## Motivation
EXP-002S48 falsified an observable residual-variance abstention repair. Its selected rule made no promotion decisions differently from frozen S46 on validation, so the added diagnostic had no causal leverage. The queue therefore redirects from another threshold/gate to a materially different inference mechanism.

## Hypothesis
The remaining heteroskedastic breadth failures arise because terminal family evidence assumes homoskedastic Gaussian residuals. A terminal-only heteroskedastic likelihood specialist that estimates variance as a function of fitted signal magnitude can improve structural inference under variance instability without changing planning or requiring a regime label.

## Frozen architecture
- Planning remains benchmark-v2 baseline-only with budget 15.
- S30 remains the anchor terminal science posterior.
- Frozen S46 coefficients and promotion rule remain the adjudication control.
- No S49 computation may use the true DAG, regime label, true nonlinear mechanism, realized edge error, or realized harm at deployment.
- Regime labels are evaluation-only.

## Specialist likelihood
For each node and candidate parent family after the completed planning trajectory:
1. fit the same Bayesian linear mean model used by benchmark v2;
2. compute fitted means and residuals on non-intervened rows;
3. fit `log(residual^2 + eps) = a + b*log1p(abs(fitted_mean))` by ridge regression;
4. convert predicted log variance to per-row variance, clipped to a frozen numerical range;
5. compute heteroskedastic Gaussian log likelihood plus a BIC penalty for the two variance parameters;
6. combine node-family scores over the exact DAG support and normalize to a posterior.

This is a terminal inference specialist only. It never feeds back into intervention selection.

## Training-only blend grid
Form `P49(beta) = (1-beta)*P_S30 + beta*P_HET`, normalized, with beta in `{0.25, 0.50, 0.75, 1.00}`.

Use fresh balanced training worlds: 48 linear + 48 heteroskedastic. Frozen S46 decides whether an alternate terminal posterior is promoted. If S46 does not promote, output the baseline posterior; if it promotes, output `P49(beta)`.

A beta qualifies on training if:
- overall S46 promotion coverage >= 0.50;
- hybrid mean edge delta versus baseline < 0 overall;
- heteroskedastic hybrid mean edge delta < 0;
- linear-anchor hybrid edge delta <= +0.02;
- overall and heteroskedastic promoted large-harm rate <= 0.05;
- hybrid mean Brier delta <= +0.005;
- at least 70% of frozen-S46/S30 structural improvement is retained overall;
- heteroskedastic hybrid edge delta is no worse than frozen S46/S30 by >0.02.

Choose the qualifying beta with the best heteroskedastic hybrid edge delta; ties within 0.01 choose the smaller beta. Persist beta before validation exposure.

## Prospective splits
- Mechanics: 4 fresh worlds, 2 linear + 2 heteroskedastic.
- Training: 96 fresh worlds, 48 + 48.
- Validation: 48 fresh worlds, 24 + 24.
- Held-out confirmation: 96 fresh worlds, 48 + 48, exposed only after validation success.

## Validation success
Require all training qualification criteria, at least 65% frozen-S46 improvement retention, and no numerical/mechanics violations.

## Confirmation promotion
Require validation success criteria plus:
- paired bootstrap 95% upper bound for hybrid edge delta < 0;
- overall and heteroskedastic promoted large-harm rate <= 0.05;
- heteroskedastic hybrid edge delta <= frozen S46/S30 heteroskedastic edge delta + 0.02;
- linear-anchor hybrid edge delta <= +0.02;
- at least 65% frozen-S46 improvement retention.

## Falsification redirect
If S49 fails, reject the fitted-magnitude heteroskedastic likelihood mechanism. Do not retry with another variance threshold. Redirect to explicit model-class uncertainty / mixture-of-world-model terminal inference or a different likelihood family with a changed causal mechanism.
