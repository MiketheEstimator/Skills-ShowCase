# EXP-002S60 Counterfactual Predictive Residual-State Representation Diagnostic

## Status
Prospective diagnostic. No deployable correction policy or threshold is fit in this experiment.

## Motivation
S59 showed that the S56-S58 residual-likelihood adjustment family is not sufficiently aligned with frozen S30 parent-ranking failures: the best observable adjustment-summary AUC was 0.5833 and only 4.3% of anchor ranking errors were repaired. A materially different representation is therefore required upstream of any new correction mechanism.

S60 tests whether **out-of-group predictive instability across observed intervention/noise states** identifies nodes where the frozen S30 family ranking is wrong. Unlike S56-S59, it does not use likelihood adjustments, variance slopes, fitted-magnitude variance, Student-t replacement, or direct residual-score substitution.

## Frozen hypothesis
Counterfactual predictive behavior across intervention/noise groups contains structural information that is lost by pooled terminal residual scores. Nodes whose anchor-selected parent family fails to transport across observed intervention states should be enriched for frozen S30 parent-ranking errors.

## Controls and invariants
- Frozen baseline planner and intervention budget 15.
- Frozen S30 terminal anchor and existing S54 world-base lineage.
- Planning traces are unchanged. S60 is terminal-only and diagnostic.
- No S56-S58 score adjustment enters the representation.
- No threshold or deployable policy is learned in S60.
- Fresh seed namespaces only.
- Ground truth is used only after all truth-free predictive features are computed, for diagnostic scoring.
- Google Drive remains read-only.

## Samples
- Mechanics: 2 linear + 2 heteroskedastic fresh worlds beginning external seed 93001.
- Diagnostic panel: 64 linear + 64 heteroskedastic fresh worlds beginning external seed 93101.

## Truth-free node representation
For each target node, enumerate all legal parent masks and use the frozen S30 family score only to identify the anchor-selected parent mask. Then perform leave-one-observed-intervention-state-out refits for every candidate family.

For each held-out intervention/noise state:
1. Refit each candidate linear family on the remaining observations only.
2. Compute held-out standardized squared prediction error using a robust train residual scale.
3. Record the anchor-selected family's held-out loss.
4. Record the best competing family's held-out loss.
5. Record whether the held-out predictive ranking disagrees with the pooled S30 family ranking.

Persist these node-level summaries:
- `selected_cv_mean_loss`: mean standardized held-out loss of the anchor-selected family.
- `selected_cv_std_loss`: standard deviation of its held-out losses across intervention states.
- `selected_cv_worst_loss`: worst held-out loss.
- `cv_rank_volatility`: fraction of held-out states where another family predicts better than the anchor-selected family.
- `cv_competitor_advantage`: mean positive held-out loss advantage of the best competitor over the anchor-selected family.
- `state_loss_range`: range of held-out anchor-selected losses across intervention states.

## Primary diagnostic metrics
- AUC of every truth-free S60 feature for detecting `anchor_rank_error`.
- Bootstrap 95% interval for the best feature AUC.
- Correlation of each feature with frozen anchor-margin severity.
- Same metrics stratified by linear and heteroskedastic regimes.
- Diagnostic integrity: exact frozen planning traces, spend <= 15, all finite outputs, and all 128 worlds completed.

## Interpretation gates
### A. `PREDICTIVE_STATE_ALIGNED`
Best feature AUC >= 0.65 and bootstrap lower bound >= 0.55.

Interpretation: counterfactual predictive transport contains useful structural error-localization information. S61 should prospectively test a bounded targeted correction/abstention mechanism using only the frozen S60 representation, with separate train/validation/confirmation splits.

### B. `PREDICTIVE_STATE_WEAK_SIGNAL`
Best feature AUC >= 0.60 but < 0.65, or AUC >= 0.65 with bootstrap lower bound < 0.55.

Interpretation: representation has partial information but is not yet reliable enough for a policy. S61 should enrich the representation with interaction/state-contrast geometry rather than fit a threshold.

### C. `PREDICTIVE_STATE_NOT_ALIGNED`
Best feature AUC < 0.60.

Interpretation: intervention-state predictive instability is not a sufficiently useful locator. S61 must change the structural representation itself, for example toward posterior family disagreement under intervention-conditioned refits, rather than retuning S60 metrics.

## Success criteria for experiment integrity
- Mechanics pass on all four mechanics worlds.
- All 128 diagnostic worlds complete.
- Frozen planning traces retained exactly.
- Ground truth excluded from feature construction.
- Disposition assigned mechanically from the preregistered gates.
- Raw node rows and summary statistics persisted.
