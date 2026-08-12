# EXP-002R7 — Local EIG vs Terminal Scientific Utility Audit

## Motivation
EXP-002R5 showed severe low-simulation EIG noise, but EXP-002R6 showed that reallocating the same planner compute toward a less noisy racing judge did not improve edge recovery and worsened Brier score / true-DAG mass despite higher MAP recovery. This shifts the dominant uncertainty from estimator variance to objective-horizon alignment.

## Hypothesis
Even when one-step EIG is estimated at high precision, ranking interventions by immediate posterior-entropy reduction per cost is weakly aligned with terminal causal-structure recovery after the remaining budget is spent.

## Design
On 6 fresh worlds, freeze the initial observational posterior and generate the normal width-2 candidate set at decision 0. Independently estimate each candidate's EIG with 30 posterior-predictive simulations. Then, for each candidate separately, force that candidate as the first real intervention and spend the remaining intervention budget using the frozen width-1 portfolio controller. Ground truth is used only after each rollout to score terminal edge error, MAP, Brier, and true-DAG mass; it is never available to proposal generation, EIG scoring, or continuation control.

## Primary diagnostic
Within each world, Spearman rank correlation between high-precision one-step EIG and negative terminal edge error across candidate interventions. Positive correlation means the local objective ranks actions consistently with better terminal edge recovery.

## Secondary diagnostics
- Terminal edge-error rank of the high-precision EIG argmax.
- Difference between terminal edge error of EIG argmax and the best candidate in hindsight.
- Corresponding correlations with terminal Brier score and true-DAG mass.

## Falsification / support
The horizon-credit mismatch hypothesis is supported at screen only if mean within-world EIG-to-terminal-edge rank correlation is near zero or negative and the EIG argmax frequently fails to land in the top terminal-recovery tier. Strong positive rank alignment falsifies this mechanism and redirects toward proposal semantics or posterior-model misspecification.

## Initial stage
6 fresh worlds. No planner parameters are tuned from results.