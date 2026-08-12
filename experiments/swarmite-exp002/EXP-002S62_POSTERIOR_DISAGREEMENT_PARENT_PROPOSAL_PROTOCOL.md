# EXP-002S62 — Posterior-Disagreement Counterfactual Parent Proposal Diagnostic

## Status
Prospective diagnostic protocol frozen before mechanics/diagnostic-panel inspection.

## Why this is the next experiment
EXP-002S61 preserved useful error localization (training AUC 0.656110) but its single counterfactual competitor was better than the anchor-selected parent family on only 29.28% of anchor-ranking-error nodes. The bounded correction therefore failed because the proposed repair direction was usually wrong. S62 changes the proposal representation itself rather than tuning S61 activation or tilt amplitude.

## Hypothesis
Intervention-conditioned refits of the ordinary local parent-family score table contain a more faithful signal about *which alternative parent family* is structurally plausible than S61's minimum mean held-out predictive-loss nomination. Averaging local parent-family posterior mass across leave-one-intervention-state-out refits should nominate competitors that are closer to the truth on anchor-ranking-error nodes, while posterior disagreement geometry should retain above-chance error localization.

## Frozen components
- Benchmark generator, candidate DAG universe, budget 15, baseline planner, S30 anchor, and S46 outer adjudication are unchanged.
- No residual-likelihood specialist, old heteroskedastic posterior, S61 tilt, or truth-derived inference input is used.
- Ground truth is used only after all observable features/proposals are frozen for diagnostic scoring.

## Observable construction
For each world and target node:
1. Build the full-data ordinary family-score table and identify the anchor-selected legal parent mask.
2. Partition rows by the same observable intervention/noise-state labels used in S60.
3. For every leave-one-state-out refit, rebuild the ordinary family-score table on the remaining states.
4. Convert the legal local family scores to a normalized local posterior with a stable log-sum-exp transform.
5. Compare each state-refit local posterior with the full-data local posterior.
6. Average state-refit posterior mass across states.
7. Nominate the non-anchor parent family with the highest mean state-refit posterior mass. This is the frozen S62 proposal; no outcome-based selection or threshold search is permitted.

## Frozen diagnostic features
- mean Jensen-Shannon divergence between state-refit and full local posteriors;
- maximum Jensen-Shannon divergence;
- full-to-refit anchor posterior-mass drop;
- nominated competitor mean posterior mass;
- nominated competitor state-MAP vote share;
- state parent-family switch rate;
- mean full-vs-refit margin erosion;
- normalized mean state-posterior entropy.

## Prospective panels
- mechanics: 2 linear + 2 heteroskedastic worlds beginning external seed 95201;
- diagnostic: 64 linear + 64 heteroskedastic worlds beginning external seed 95301.

No correction policy is fitted in S62. This prevents a proposal diagnostic from becoming a post-hoc policy search.

## Primary diagnostic outcomes
1. Best truth-free posterior-disagreement feature AUC for frozen anchor local parent-ranking error, with bootstrap 95% interval.
2. Nominated-competitor usefulness fraction on anchor-ranking-error nodes: fraction where the nominated parent mask has smaller parent-set Hamming error to truth than the anchor-selected parent mask.
3. Exact-truth nomination rate on anchor-ranking-error nodes.
4. Usefulness by linear vs heteroskedastic regime.
5. Mean number of usable leave-one-state-out refits and mechanics/reproducibility checks.

## Preregistered disposition
- `POSTERIOR_DISAGREEMENT_ALIGNED`: best AUC >= 0.60, bootstrap lower bound >= 0.55, and competitor usefulness on anchor-error nodes > 0.50.
- `ERROR_LOCALIZATION_ONLY`: AUC criteria pass but competitor usefulness <= 0.50.
- `PROPOSAL_ONLY`: competitor usefulness > 0.50 but AUC criteria fail.
- `POSTERIOR_DISAGREEMENT_NOT_ALIGNED`: neither criterion passes.
- `BLOCKED_EXECUTION_MECHANICS`: mechanics/reproducibility fails.

## Successor logic
- ALIGNED -> S63 prospectively tests a bounded correction using the S62 posterior-mass proposal, without retuning S61.
- ERROR_LOCALIZATION_ONLY -> S63 changes from a single nominated competitor to a set-valued/top-family uncertainty representation; no threshold tuning.
- PROPOSAL_ONLY -> S63 combines the frozen S60 localization representation with the independently supported S62 proposal mechanism.
- NOT_ALIGNED -> S63 abandons leave-one-state-out local family nomination and tests intervention-contrast conditional independence / invariance as a materially different structural representation.

Scientific falsification is a completed result and immediately redirects the queue.