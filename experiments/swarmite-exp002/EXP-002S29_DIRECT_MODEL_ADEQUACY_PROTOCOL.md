# EXP-002S29 — Direct Predictive Model-Adequacy Score Diagnostic

## Status
Exploratory diagnostic frozen before computing row-level adequacy scores.

## Motivation
S28 falsified classification from posterior disagreement plus summary residual features. S29 changes the observable representation rather than tuning classifiers: estimate which likelihood/mechanism class generalizes better by direct cross-validated predictive scoring on the terminal dataset.

## Data boundary
Use only S27 held-out confirmation seeds 71300-71395. These worlds remain diagnostic-only and are permanently excluded from any successor selector's training/validation/confirmation sets.

## Observable score
Reconstruct each terminal dataset exactly with the frozen S25 baseline planner. For each node and each of 5 deterministic folds, compare two model classes using only training-fold data to select the parent subset:

1. **Baseline class:** linear parents, Gaussian residual model with unit noise, ridge prior precision inherited from benchmark `TAU2`.
2. **Robust class:** `tanh(parent)` features with frozen Student-t3 likelihood/scale and ridge prior, using the exact S23 fitting mechanics.

For each class, select the node parent subset with best training score using that class's frozen scoring rule, then evaluate predictive log likelihood on the held-out fold. Intervention rows targeting the evaluated node are excluded exactly as in benchmark family fitting.

Sum held-out node scores across folds. Define deployment-eligible adequacy statistic:

`ADEQ = CV_log_score_robust - CV_log_score_baseline`.

No ground-truth DAG, regime label, terminal edge error, seed modulo, or future outcome contributes to ADEQ.

## Diagnostic target
Primary: whether frozen robust terminal inference improves edge error over baseline, `1(edge_delta < 0)`, taken only as an evaluation label from S27.
Secondary: large harm `1(edge_delta > 0.50)`.

## Frozen analyses
- ROC AUC of ADEQ for robust-beneficial label.
- Balanced accuracy for the natural zero boundary `ADEQ > 0`.
- AUC separately reported against prior S28 features for context only; no combined feature fitting.
- Regime-stratified ADEQ medians and false-selection counts for interpretation only.
- Spearman rank correlation between ADEQ and robust edge delta.

## Diagnostic success criterion
Direct predictive adequacy is promising only if all hold:
1. AUC >= 0.70 for robust-beneficial label.
2. Balanced accuracy at ADEQ>0 >= 0.65.
3. ADEQ is finite on all worlds and terminal-data reconstruction is exact.

If supported, enqueue a fresh-world fixed ADEQ selector with separated train/validation/confirmation and no tuning on S27-S29 worlds.
If unsupported, do not add thresholds or combine ADEQ with the previously falsified residual summaries. Redirect toward posterior combination/decision-theoretic model uncertainty rather than per-world hard selection.
