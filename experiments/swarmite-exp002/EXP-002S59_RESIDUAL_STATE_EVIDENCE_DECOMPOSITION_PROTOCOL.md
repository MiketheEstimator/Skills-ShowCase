# EXP-002S59 Residual-State Evidence Decomposition Diagnostic

## Status
Prospective diagnostic. No deployable policy or threshold is fit in this experiment.

## Motivation
S56-S58 produced nontrivial residual-process evidence but all three likelihood substitutions were structurally harmful. S58 in particular adjusted almost every family and worsened the matched hybrid edge metric. Before introducing another likelihood family, test whether observable residual-state evidence is actually concentrated where the frozen S30 family ranking is wrong and whether the S58 score correction points in the right direction.

## Frozen hypothesis
Residual-state evidence contains local information about parent-set ranking failures even though direct likelihood substitution is miscalibrated.

## Controls and invariants
- Frozen baseline planner and intervention budget 15.
- Frozen S30 terminal anchor and S46 outer promotion control through the existing S54 world-base lineage.
- Frozen S58 intervention-conditional residual score construction. No refitting of NU, shrinkage, clipping, thresholds, or intervention policy.
- Fresh seed namespaces only.
- Ground truth is used only after terminal inference to score diagnostic alignment. It is never an input to planning or residual evidence construction.
- Google Drive remains read-only.

## Samples
- Mechanics: 2 linear + 2 heteroskedastic fresh worlds beginning external seed 92001.
- Diagnostic panel: 64 linear + 64 heteroskedastic fresh worlds beginning external seed 92101.

## Node-level quantities
For every target node in every world:
1. `anchor_margin`: frozen Gaussian family score of the true parent set minus the best competing parent-set score.
2. `anchor_rank_error`: indicator that `anchor_margin < 0`.
3. `s58_margin`: S58-adjusted family score of the true parent set minus the best competing adjusted score.
4. `correction_delta`: `s58_margin - anchor_margin`.
5. Observable, truth-free residual-state summaries computed across candidate parent sets for the node: mean absolute S58 adjustment, standard deviation of adjustments, adjustment range, and fraction with |adjustment| >= 0.02.

## Primary diagnostic metrics
- AUC of each observable residual-state summary for detecting `anchor_rank_error` across nodes.
- Point-biserial/correlation of each observable summary with anchor margin severity (`-anchor_margin`).
- Among anchor-rank-error nodes: mean `correction_delta`, fraction with positive correction, and fraction whose ranking is actually repaired by S58.
- Same metrics stratified by linear vs heteroskedastic regime.
- Bootstrap 95% interval for the best observable AUC and for mean correction delta among anchor-error nodes.

## Interpretation gates
This is a diagnostic, so falsification is a valid completion.

### A. `EVIDENCE_ALIGNED_DIRECTION_WRONG`
Best observable error-detection AUC >= 0.65, but mean correction delta among anchor-error nodes <= 0 or fewer than 55% of error nodes receive a positive correction.
Successor must preserve the useful detection representation while changing how evidence affects family ranking. Do not create another direct residual likelihood.

### B. `EVIDENCE_ALIGNED_PARTIAL_CORRECTION`
Best observable AUC >= 0.65, mean correction delta among anchor-error nodes > 0, and >=55% receive positive correction, but fewer than 50% of anchor errors are fully repaired.
Successor should learn/bound a targeted correction or abstention mechanism from the diagnostic representation without globally replacing the likelihood.

### C. `EVIDENCE_ALIGNED_CORRECTION_SUPPORTED`
Best observable AUC >= 0.65 and at least 50% of anchor rank errors are repaired with positive mean correction.
Successor may prospectively test a bounded targeted family-rank correction with separate training/validation/confirmation.

### D. `EVIDENCE_NOT_ALIGNED`
Best observable AUC < 0.65.
Abandon the S56-S58 residual-state evidence family as the primary structural signal. Successor must change representation upstream, not retune the same likelihood.

## Success criteria for experiment integrity
- Mechanics pass on all four mechanics worlds.
- All terminal posteriors finite and normalized.
- Exact frozen planning traces retained.
- All 128 diagnostic worlds completed.
- Disposition assigned by the gates above with raw node-level diagnostic rows persisted.
