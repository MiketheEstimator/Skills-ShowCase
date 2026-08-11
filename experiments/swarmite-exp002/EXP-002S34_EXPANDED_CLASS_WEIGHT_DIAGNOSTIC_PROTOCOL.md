# EXP-002S34 — Expanded-Class Weight Attribution Diagnostic

## Status
PENDING until execution workflow marks RUNNING.

## Rationale
S33 expanded the terminal model set to seven mechanism×noise classes but prospectively worsened mean edge recovery versus both the frozen S30 mixture and baseline, despite improving mean Brier. The Gaussian nonlinear classes received most of the predictive weight while the Student-t robust classes received little. Before changing temperature, adding classes, or retraining a selector, isolate whether the failure is caused by predictive-weight misalignment, mixture dilution, or residual model-set insufficiency.

## Frozen diagnostic questions
On the completed S33 screen worlds only (seeds 72111–72146), reconstruct each of the seven S33 class posteriors without changing observations or planning and evaluate terminal metrics using ground truth **only for retrospective diagnosis**.

For each world record:
- terminal edge error and Brier for each class;
- class predictive CV score and S33 weight;
- oracle-best represented class by edge error;
- top-predictive-weight class;
- rank correlation between predictive score and negative terminal edge error across classes;
- S30 edge error, expanded-mixture edge error, and oracle-best class edge error;
- mixture regret versus oracle represented class;
- whether any represented class beats S30.

## Diagnostic dispositions
1. `PREDICTIVE_WEIGHT_MISALIGNMENT` if mean within-world Spearman(score, -edge_error) < 0.20 OR top-weight class equals oracle-best in < 25% of worlds, while at least one represented class beats S30 in >= 60% of worlds.
2. `CLASS_DILUTION` if mean Spearman >= 0.20 and represented-class coverage >= 60%, but expanded-mixture regret versus the oracle represented class is >= 0.20 edge-error units.
3. `MODEL_SET_INSUFFICIENCY` if fewer than 60% of worlds contain any represented class that beats S30.
4. `MIXED_FAILURE` otherwise.

These categories are diagnostic, not deployment rules.

## Success criterion
S34 is scientifically complete when the reconstruction mechanics pass and one disposition is assigned from the frozen rules. No claim of treatment superiority is made.

## Invariants
- No new worlds or tuning.
- No threshold/temperature optimization.
- Same evidence and action traces as S33.
- Truth enters only retrospective diagnostic metrics.
- Preserve all negative results and lineage.
- Google Drive remains read-only.
