# EXP-002R9 — Edge-Centric Expected Utility Audit

## Motivation
EXP-002R8 falsified the preregistered edge-uncertainty regime moderator. Across 12 prospective validation worlds, initial mean edge uncertainty did not explain when one-step DAG-entropy EIG aligned with terminal edge recovery. The broader pattern from R6-R8 is that the current planner objective can improve MAP while worsening edge error, Brier score, and true-DAG mass, suggesting objective mismatch rather than a simple state gate.

## Hypothesis
A posterior-predictive objective tied directly to edge-marginal uncertainty will align more strongly with terminal edge recovery than the current whole-DAG entropy EIG objective.

## Design
On 6 fresh diagnostic worlds, freeze the initial observational posterior and normal width-2 decision-0 candidate set. For each candidate, use 30 independent posterior-predictive simulations to estimate two quantities per intervention cost: (1) current DAG-entropy EIG and (2) expected reduction in total Bernoulli edge entropy across the 20 directed edge marginals. Then force each candidate as the first real intervention and complete the remaining intervention budget with the frozen width-1 controller exactly as in EXP-002R7.

## Primary diagnostic
Within each world, compare Spearman rank correlation with negative terminal edge error for edge-entropy utility versus DAG-entropy EIG. Primary paired quantity is `rho_edge_utility - rho_dag_eig` across worlds.

## Secondary diagnostics
Compare rank alignment to terminal Brier score and true-DAG mass; compare terminal rank/regret of each objective's argmax; record candidate action duplicates separately but do not tune proposal generation.

## Success criterion
Promote an edge-centric planner objective only if mean paired rank-alignment improvement is positive and at least 4 of 6 worlds improve, with no evidence that the improvement is solely caused by duplicate proposal aliases. Otherwise falsify this reward change and redirect to proposal semantics / model calibration.

## Initial stage
Fixed fresh seeds 56001 through 56006. No planner parameters are tuned from outcomes.