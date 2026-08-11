# EXP-002S48 — Regime-Localized Heteroskedastic Robustness Repair

## Motivation
EXP-002S47 falsified breadth promotion of the frozen S46 architecture. The failure was localized: the heteroskedastic regime was the only breadth cell with promoted large harm (16.7% in the screen), while linear, weak-effect, compound-t, topology, and joint cells had zero promoted large harms. This experiment therefore does not globally refit S46.

## Hypothesis
The remaining S46 breadth failure is driven by observable conditional-variance instability that is not represented in the S46 feature vector. A residual heteroskedasticity diagnostic can selectively tighten the frozen S46 promotion rule on variance-unstable worlds while preserving the original rule elsewhere.

## Frozen anchor
- Planning remains benchmark-v2 baseline-only, budget 15.
- Terminal science posterior remains frozen S30.
- The S46 model coefficients, standardization, and selected rule are frozen.
- No S48 feature may use the true DAG, regime label, true mechanism, realized edge error, or realized harm at deployment.

## New observable diagnostic
After the fixed planning trajectory, compute a heteroskedasticity score from the baseline MAP-DAG family regressions. For each node, using only rows where that node was not intervened upon:
1. compute fitted values and squared residuals;
2. split observations at the median absolute fitted magnitude;
3. compute log residual-variance ratio, high-magnitude versus low-magnitude;
4. compute Pearson correlation between absolute fitted magnitude and squared residual.
The world score is the maximum across nodes of `max(0, log_variance_ratio) + max(0, correlation)`.

## Training-only repair grid
Fresh balanced training worlds contain only the localized failing regime and a linear-Gaussian anchor: 48 heteroskedastic + 48 linear worlds.

Candidate heteroskedasticity thresholds are the training 50th, 65th, 80th, and 90th percentiles. When the frozen S46 rule already promotes a world and its heteroskedasticity score exceeds the threshold, apply a stricter S30 condition: predicted edge delta <= -0.10 and predicted large-harm probability <= one of {0.05, 0.10}. Otherwise preserve the frozen S46 decision exactly.

A candidate qualifies on training if:
- overall coverage >= 0.50;
- heteroskedastic coverage >= 0.40;
- promoted large-harm rate <= 0.05 overall and within heteroskedastic worlds;
- hybrid mean edge delta < 0 overall and separately in both regimes;
- hybrid mean Brier delta <= +0.005;
- at least 70% of the frozen S46 hybrid structural improvement is retained;
- linear-anchor hybrid edge delta is no worse than frozen S46 by >0.02.

Choose the qualifying candidate with highest retained improvement; ties within 0.01 choose the lower heteroskedasticity threshold, then lower harm cutoff. Persist the selected rule before validation exposure.

## Prospective splits
- Training: 96 fresh balanced worlds, 48 linear + 48 heteroskedastic.
- Validation: 48 fresh balanced worlds, 24 + 24.
- Held-out confirmation: 96 fresh balanced worlds, 48 + 48, exposed only if validation passes.

## Validation success
All mechanics invariants plus the training qualification criteria, with heteroskedastic promoted large-harm rate <= 0.05 and at least 65% frozen-S46 improvement retention.

## Confirmation promotion
Require validation success criteria plus:
- paired bootstrap 95% upper bound for hybrid edge delta < 0;
- overall and heteroskedastic promoted large-harm rate <= 0.05;
- at least 65% frozen-S46 improvement retention;
- linear-anchor degradation versus frozen S46 <= 0.02 edge-error units.

## Interpretation
Success supports targeted residual-variance protection as an add-on uncertainty feature around S46. Failure rejects this localized conditional-variance diagnostic and redirects to a materially different robustness mechanism rather than global S46 refitting or another generic threshold search.
