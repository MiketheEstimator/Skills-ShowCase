# EXP-002S28 — Selector Error Representation Diagnostic

## Status
Exploratory diagnostic preregistered before inspecting S27 confirmation row-level features.

## Motivation
S27's frozen one-dimensional `PPC_tail > 6` selector protected every linear-Gaussian confirmation world and achieved significant aggregate improvement, but failed promotion because robust selection was too sparse in shifted regimes, with softsign+t5 unresolved. Before training another selector, determine whether the already-computed observable diagnostics contain incremental information about when robust terminal inference outperforms baseline.

## Data boundary
Use only the already-completed S27 held-out confirmation rows (seeds 71300-71395) for **exploratory diagnosis**. These rows are permanently excluded from training or validating any successor selector. No new efficacy claim is permitted from S28.

## Observable features
Deployment-eligible features only:
- `D_robust`
- `log1p(PPC_tail)`
- `PPC_nonlinear`

Forbidden predictors: regime label, seed modulo, DAG truth, edge delta, Brier delta, posterior quality, or any future outcome. Those may be used only as diagnostic labels/strata.

## Diagnostic targets
Primary target: `robust_beneficial = 1(edge_delta < 0)`.
Secondary target: `robust_harmful = 1(edge_delta > 0.50)`.

## Frozen analyses
1. Compute rank/AUC discrimination for each single observable feature against `robust_beneficial`.
2. Compare deterministic 8-fold cross-validated logistic models:
   - tail-only: standardized `log1p(PPC_tail)`;
   - multivariate: standardized `[D_robust, log1p(PPC_tail), PPC_nonlinear]`.
3. Folds are fixed by sorted seed order modulo 8; standardization and fitting occur inside each training fold only.
4. Logistic fitting is deterministic full-batch gradient descent: learning rate 0.05, 3000 iterations, L2=0.10, intercept unpenalized.
5. Report out-of-fold ROC AUC, balanced accuracy at probability 0.50, confusion counts, and regime-stratified false-negative/false-positive counts for interpretation only.
6. Report feature correlations and medians separately for robust-beneficial and non-beneficial worlds.

## Success criterion for representation
Multivariate observable representation is considered diagnostically promising only if:
- out-of-fold multivariate AUC >= 0.70;
- multivariate AUC exceeds tail-only AUC by >= 0.05;
- no mechanics/provenance invariant is violated.

If supported, enqueue a **fresh-world** preregistered multivariate selector with new training/validation/confirmation seeds. Do not fit its final parameters on S27/S28 worlds.

If not supported, do not tune thresholds or classifier hyperparameters on these worlds. Redirect to a materially different observable representation of model adequacy or posterior conflict.
