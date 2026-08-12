# EXP-002S18R — Residual-Dependence Gate Recovery

## Status
RUNNING after protocol freeze.

## Purpose
Recover the S18 scientific question without using its exposed validation worlds. S18 training is permanently nonpoolable for threshold selection because the highest-coverage rule tied R<=0.50 and R<=infinity without a preregistered tie-break.

## Frozen architecture
Identical to S18: S17 latent-confounding worlds with rho=0.60; benchmark-v2 planning; frozen nonlocal terminal science posterior; frozen D<=1.50 requirement; residual-dependence score R computed from observational-row residual correlations under the baseline MAP DAG.

## Training
Use entirely fresh seeds 69401-69424. Candidate R thresholds {0.15,0.20,0.25,0.30,0.35,0.40,0.50,infinity}. Passing thresholds require coverage>=0.50, promoted mean edge delta<=-0.10, promoted mean Brier delta<=+0.005, and <=2 promoted large harms. Select the highest-coverage passing threshold. **Frozen tie-break:** if coverage ties, select the smaller finite R threshold; if metrics and inclusion sets are identical this still chooses the smaller threshold. Persist selection before validation.

## Validation
Fresh seeds 69501-69524. Pass if coverage>=0.50, promoted mean edge delta<=-0.10, promoted mean Brier delta<=+0.005, <=2 promoted large harms, and exact trace identity.

## Confirmation
Only if validation passes: seeds 69601-69648. Require coverage>=0.50, promoted mean edge delta<=-0.10, bootstrap 95% upper bound<0, promoted mean Brier delta<=+0.005, <=4 promoted large harms, and trace identity.

## Redirect
If falsified, conclude residual-dependence threshold stacking is insufficient and redirect to an explicit latent-variable science model.