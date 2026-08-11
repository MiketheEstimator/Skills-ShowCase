# EXP-002S18 — Residual-Dependence Augmented Abstention Gate

## Status
RUNNING after protocol freeze.

## Hypothesis
S17 shows that baseline-vs-science posterior disagreement alone does not fully detect omitted latent confounding. A second observable model-check signal, residual dependence under the baseline MAP DAG, can identify worlds where causal sufficiency is doubtful and improve calibration of promoted structural conclusions without changing planning or inference.

## Frozen architecture
Use the exact S17 latent-confounding worlds with rho=0.60, benchmark-v2 planning, frozen S10/S5 terminal science posterior, and frozen S15 disagreement requirement D<=1.50.

After the final observation, rebuild baseline family models and take the baseline posterior MAP DAG. On the original observational rows only, compute each node's regression residual under its MAP parent set. Define `R=max(abs(corr(residual_i,residual_j)))` over node pairs. Structural promotion requires both D<=1.50 and R<=R_threshold. Otherwise return ABSTAIN_MODEL_SHIFT. Neither D nor R may affect planning.

## Training
Fresh seeds 69101-69124. Candidate R thresholds: {0.15,0.20,0.25,0.30,0.35,0.40,0.50,infinity}. Select the highest-coverage threshold satisfying coverage>=0.50, promoted mean edge delta<=-0.10, promoted mean Brier delta<=+0.005, and <=2 promoted large harms. Freeze threshold before validation.

## Validation
Fresh seeds 69201-69224. Pass if coverage>=0.50, promoted mean edge delta<=-0.10, promoted mean Brier delta<=+0.005, <=2 promoted large harms, and exact trace identity.

## Confirmation
Only if validation passes: seeds 69301-69348. Require coverage>=0.50, promoted mean edge delta<=-0.10, bootstrap 95% upper bound<0, promoted mean Brier delta<=+0.005, <=4 promoted large harms, and exact trace identity.

## Redirect
If falsified, residual-correlation diagnostics are insufficient; redirect toward an explicit latent-variable structural science model rather than additional threshold stacking.