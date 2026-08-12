# EXP-002S67 — Intervention-Response Disagreement Acquisition Diagnostic

## Status
Prospective protocol frozen before mechanics or held-out acquisition inspection.

## Scientific basis
S66 falsified the S62/S65 scalar anchor-error probability as an acquisition signal: held-out positive-value AUC was 0.5451, Spearman correlation 0.1159, and evidence-selected mean realized value-per-cost (0.0682) underperformed the frozen EIG target (0.0786). This does not falsify planning-side improvement in general; it falsifies reusing a terminal localization probability as a scalar acquisition utility.

## Hypothesis
Targets whose competing structural hypotheses predict materially different posterior responses to feasible interventions should have greater realized acquisition value than targets chosen from static terminal localization. A truth-free intervention-response disagreement score can therefore identify useful intervention targets without modifying terminal posterior geometry.

## Frozen components
- benchmark/data generators, intervention costs, legal DAG universe, and budget;
- baseline planner and frozen EIG comparator;
- S30 terminal posterior and all terminal inference logic remain unchanged;
- S66 realized acquisition-value definition and fresh world-generation representation;
- no S62/S65 localization probabilities enter the S67 score;
- ground truth is used only after candidate interventions are generated and inferred, to score realized acquisition value.

## S67 disagreement representation
For each candidate target node at the already-observed terminal state:
1. Rebuild the ordinary family-model likelihood posterior and predictive family models from observable data only.
2. For each setpoint in {-2,+2}, draw a fixed deterministic panel of posterior-predictive intervention outcomes from the ordinary posterior.
3. Update the ordinary posterior for each simulated outcome without changing the actual data.
4. Convert each updated posterior to edge marginals.
5. Compute two truth-free components:
   - within-setpoint response dispersion: mean edge-marginal variance across posterior-predictive outcomes;
   - cross-setpoint structural separation: mean absolute difference between the average edge-marginal response at -2 and +2.
6. Define disagreement utility as `(dispersion + separation) / intervention_cost`.

This representation asks whether plausible intervention responses disagree structurally, rather than whether the current terminal graph is probably wrong.

## Prospective panels
- mechanics: 2 linear + 2 heteroskedastic worlds beginning 100201;
- held-out acquisition diagnostic: 64 linear + 64 heteroskedastic worlds beginning 100401.
No learned parameters are fit in S67.

## Metrics
- AUC of disagreement utility for positive realized acquisition value;
- Spearman correlation between disagreement utility and realized acquisition value-per-cost;
- mean realized value-per-cost of disagreement-selected target versus frozen EIG-selected target;
- paired mean difference and fraction of worlds disagreement selection beats EIG;
- regime-specific paired differences;
- mechanics, finite posterior, trace identity, and spend checks.

## Qualification / disposition
`RESPONSE_DISAGREEMENT_ALIGNED` requires mechanics pass; held-out AUC >= 0.60; Spearman >= 0.10; disagreement-selected mean value-per-cost >= frozen EIG mean value-per-cost; and no regime paired difference < -0.02.

`RESPONSE_DISAGREEMENT_WEAK` applies when AUC >= 0.56 but the full aligned gate fails. This can justify a materially new uncertainty-aware set-valued acquisition policy, not score-temperature or threshold tuning.

`RESPONSE_DISAGREEMENT_FALSIFIED` applies when AUC < 0.56 or Spearman <= 0. It redirects away from static/posterior-response scalar target scores toward a sequential value-of-information representation that explicitly models intervention outcome branches.

Execution failures are BLOCKED and repaired without opening new scientific panels. Scientific falsification is a completed result and immediately triggers a materially different successor.