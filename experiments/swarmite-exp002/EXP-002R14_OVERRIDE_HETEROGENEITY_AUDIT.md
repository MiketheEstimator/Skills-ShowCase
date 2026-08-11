# EXP-002R14 — Exploratory Override Heterogeneity Audit

## Status
COMPLETE_EXPLORATORY_DIAGNOSTIC. This is explicitly post-hoc and is not confirmatory evidence.

## Motivation
EXP-002R13 improved mean edge error but failed its 8/12 strict-win criterion and had a confidence interval crossing zero. The treatment changed the one-step action in 8/12 worlds: 5 changes helped and 3 hurt.

## Exploratory diagnostics on changed-decision worlds
- Terminal-score advantage versus realized edge-error delta: Pearson r = -0.196.
- One-step EIG gap between control and treatment versus realized edge-error delta: Pearson r = -0.329.
- Intervention-cost increase versus realized edge-error delta: Pearson r = +0.526, driven by the sole higher-cost override (seed 60012), which was harmful.

## Interpretation
Neither a larger terminal-score margin nor a smaller one-step disagreement gap cleanly separates helpful from harmful overrides in the eight changed worlds. A simple confidence-threshold gate would therefore be a weakly justified retry. The most concrete mechanistic signal is cost sensitivity: R13's large beneficial overrides all stayed within the control action's intervention-cost tier, whereas the sole cost-increasing override was harmful. Because this is one observation, it requires fresh prospective validation rather than policy promotion.

## Successor direction
Prospectively test cost-tier-constrained selective terminal rescoring: treatment may override the one-step argmax only with a candidate of equal or lower intervention cost. This changes the admissible mechanism rather than merely retuning an R13 score threshold.