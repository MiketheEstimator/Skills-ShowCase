# EXP-002S66 — Evidence-Guided Intervention Allocation Diagnostic

## Status
Prospective protocol frozen before mechanics or held-out acquisition inspection.

## Scientific basis
S62-S65 repeatedly preserve useful prospective localization/proposal evidence while falsifying four different terminal-use geometries (bounded correction, exponential tilt, constrained projection, and Bayes structural action). S65 retained AUC 0.7187 and proposal usefulness 0.6416 but worsened paired action-edge error by +0.1406 with 2 candidate large harms versus 0 control harms. The next justified question is therefore whether the signal is useful upstream for deciding where to acquire information rather than downstream for changing inference.

## Hypothesis
A node assigned high frozen S62/S65 anchor-error probability should have greater expected value from an additional intervention on that node, measured as reduction in terminal S30 edge error per unit intervention cost. If this relationship generalizes prospectively, the signal can be redirected into planning without altering terminal posterior geometry.

## Frozen components
- benchmark/data generators and legal DAG universe;
- baseline planner, intervention costs, S30 terminal posterior, S46 outer logic, and S62 feature construction;
- S65 ridge-logistic localization model form;
- no S63/S64/S65 posterior or action modification;
- truth is used only after candidate interventions are generated and inferred, for scoring realized acquisition value.

## Diagnostic mechanism
1. Fit the frozen-form S65 localization model on a fresh 64 linear + 64 heteroskedastic training panel.
2. On a disjoint diagnostic panel, compute each node's predicted anchor-error probability from observable S62 features.
3. For every target node, execute two deterministic one-row counterfactual interventions at setpoints -2 and +2 from the already-observed terminal state, using the correct world environment only as the simulator.
4. Rebuild the ordinary likelihood posterior and S30 posterior after each row; do not use truth in inference.
5. Define realized acquisition value as mean reduction in S30 terminal edge error divided by the frozen intervention cost.
6. Compare node localization probability with positive acquisition value and continuous acquisition value.
7. As a planning-oriented matched diagnostic, compare the target selected by highest predicted-error-per-cost with the target selected by the frozen baseline planner's highest EIG-per-cost proposal, using realized value-per-cost. This is a diagnostic comparison, not a deployable policy claim.

## Prospective panels
- mechanics: 2 linear + 2 heteroskedastic worlds beginning 99201;
- localization-model training: 64 + 64 worlds beginning 99301;
- held-out acquisition diagnostic: 64 + 64 worlds beginning 99701.

## Metrics
- AUC of predicted anchor-error probability for positive realized acquisition value;
- Spearman correlation between probability and realized acquisition value-per-cost;
- mean realized value-per-cost of evidence-selected target versus frozen EIG-selected target;
- fraction of worlds evidence-selected target exceeds EIG-selected target;
- results by linear and heteroskedastic regime;
- mechanics, finite posterior, trace identity, and spend checks.

## Qualification / disposition
`ALLOCATION_SIGNAL_ALIGNED` requires: mechanics pass; held-out AUC >= 0.60; Spearman >= 0.10; evidence-selected mean value-per-cost >= EIG-selected mean value-per-cost; and no regime has evidence-selected mean value-per-cost worse than EIG by more than 0.02 edge-error units per cost.

`ALLOCATION_SIGNAL_WEAK` applies when AUC >= 0.56 but the full aligned gate fails. This may justify a materially new uncertainty-aware acquisition representation, but not threshold tuning.

`ALLOCATION_SIGNAL_FALSIFIED` applies when AUC < 0.56 or correlation is non-positive and redirects away from S62/S65 scalar localization for planning.

Execution failures are BLOCKED and must be repaired without opening new scientific panels. Scientific falsification is a completed result and immediately triggers a materially different successor.
